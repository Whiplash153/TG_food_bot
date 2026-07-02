from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from app.db.database import SessionLocal
from app.keyboards.main_keyboard import MAIN_MENU_KEYBOARD
from app.services.content import ContentService
from app.services.user import UserService


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user is None or update.message is None:
        return

    with SessionLocal() as session:
        user_service = UserService(session)
        user_service.create_or_update_user(update.effective_user)

        content_service = ContentService(session)
        text = content_service.get_main_menu_text()

    await update.message.reply_text(
        text=text,
        reply_markup=MAIN_MENU_KEYBOARD,
    )


def get_user_handlers() -> list[CommandHandler]:
    return [CommandHandler("start", start)]
