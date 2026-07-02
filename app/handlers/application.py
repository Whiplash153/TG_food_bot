import logging

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from telegram.error import TelegramError

from app.config.settings import settings
from app.db.database import SessionLocal
from app.errors import ValidationError
from app.keyboards.main_keyboard import APPLICATION_FORM_KEYBOARD, MAIN_MENU_KEYBOARD
from app.services.application import ApplicationService
from app.services.user import UserService


FORM_DATA_KEY = "application_form"
CURRENT_FIELD_KEY = "application_current_field"

logger = logging.getLogger(__name__)


async def start_application(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    with SessionLocal() as session:
        application_service = ApplicationService(session)

        first_field = application_service.get_first_field()
        start_text = application_service.get_start_text()
        field_prompt = application_service.get_field_prompt(first_field)

    context.user_data[FORM_DATA_KEY] = {}
    context.user_data[CURRENT_FIELD_KEY] = first_field

    await update.message.reply_text(
        text=f"{start_text}\n\n{field_prompt}",
        reply_markup=APPLICATION_FORM_KEYBOARD,
    )


async def cancel_application(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    context.user_data.pop(FORM_DATA_KEY, None)
    context.user_data.pop(CURRENT_FIELD_KEY, None)

    await update.message.reply_text(
        text="Заполнение заявки отменено.",
        reply_markup=MAIN_MENU_KEYBOARD,
    )


async def handle_application_field(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None or update.message.text is None:
        return

    form_data = context.user_data.get(FORM_DATA_KEY)
    current_field = context.user_data.get(CURRENT_FIELD_KEY)

    if form_data is None or current_field is None:
        return

    user_text = update.message.text

    with SessionLocal() as session:
        application_service = ApplicationService(session)

        if user_text == "Пропустить":
            if not application_service.can_skip_field(current_field):
                await update.message.reply_text(
                    text="Это поле обязательно. Введите значение.",
                    reply_markup=APPLICATION_FORM_KEYBOARD,
                )
                return

            value = None
        else:
            try:
                value = application_service.validate_field(
                    field=current_field,
                    value=user_text,
                )
            except ValidationError as error:
                await update.message.reply_text(
                    text=str(error),
                    reply_markup=APPLICATION_FORM_KEYBOARD,
                )
                return

        form_data[current_field] = value

        next_field = application_service.get_next_field(current_field)

        if next_field is None:
            if update.effective_user is None:
                return

            user_service = UserService(session)
            user = user_service.create_or_update_user(update.effective_user)

            application = application_service.create_application(
                user_id=user.id,
                form_data=form_data,
            )

            notification_text = application_service.get_manager_notification_text(
                application
            )

            try:
                await context.bot.send_message(
                    chat_id=settings.manager_chat_id,
                    text=notification_text,
                )
            except TelegramError as error:
                logger.warning(
                    "Failed to send application notification: application_id=%s, "
                    "manager_chat_id=%s, error=%s",
                    application.id,
                    settings.manager_chat_id,
                    error,
                )
                application_service.mark_notification_failed(application)
            else:
                logger.info(
                    "Application notification sent: application_id=%s, "
                    "manager_chat_id=%s",
                    application.id,
                    settings.manager_chat_id,
                )
                application_service.mark_notification_sent(application)

            context.user_data.pop(FORM_DATA_KEY, None)
            context.user_data.pop(CURRENT_FIELD_KEY, None)

            await update.message.reply_text(
                text=application_service.get_success_text(),
                reply_markup=MAIN_MENU_KEYBOARD,
            )
            return

        context.user_data[CURRENT_FIELD_KEY] = next_field
        next_prompt = application_service.get_field_prompt(next_field)

    await update.message.reply_text(
        text=next_prompt,
        reply_markup=APPLICATION_FORM_KEYBOARD,
    )


def get_application_command_handlers() -> list[MessageHandler]:
    return [
        MessageHandler(filters.Regex("^📝 Оставить заявку$"), start_application),
        MessageHandler(filters.Regex("^Отменить заявку$"), cancel_application),
    ]


def get_application_form_handlers() -> list[MessageHandler]:
    return [
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_application_field),
    ]
