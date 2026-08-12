import logging

from telegram import Update
from telegram.ext import Application, ApplicationBuilder, ContextTypes

from app.config.settings import settings
from app.handlers.application import (
    get_application_command_handlers,
    get_application_form_handlers,
)
from app.handlers.content import get_content_handlers
from app.handlers.user import get_user_handlers


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Unhandled error while processing update", exc_info=context.error)

    if isinstance(update, Update) and update.message is not None:
        await update.message.reply_text(
            "Произошла ошибка. Попробуйте ещё раз или вернитесь в главное меню."
        )


def register_handlers(application: Application) -> None:
    for handler in get_user_handlers():
        application.add_handler(handler)

    for handler in get_content_handlers():
        application.add_handler(handler)

    for handler in get_application_command_handlers():
        application.add_handler(handler)

    for handler in get_application_form_handlers():
        application.add_handler(handler)


def main() -> None:
    application = ApplicationBuilder().token(settings.bot_token).build()

    register_handlers(application)
    application.add_error_handler(error_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
