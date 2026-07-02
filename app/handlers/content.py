from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from app.db.database import SessionLocal
from app.keyboards.main_keyboard import MAIN_MENU_KEYBOARD
from app.services.content import ContentService


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    with SessionLocal() as session:
        content_service = ContentService(session)
        text = content_service.get_main_menu_text()

    await update.message.reply_text(
        text=text,
        reply_markup=MAIN_MENU_KEYBOARD,
    )


async def show_promotions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    with SessionLocal() as session:
        content_service = ContentService(session)
        promotions = content_service.get_active_promotions()
        text = content_service.format_promotions(promotions)

    await update.message.reply_text(
        text=text,
        reply_markup=MAIN_MENU_KEYBOARD,
    )


async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    with SessionLocal() as session:
        content_service = ContentService(session)
        text = content_service.get_about_text()

    await update.message.reply_text(
        text=text,
        reply_markup=MAIN_MENU_KEYBOARD,
    )


async def show_faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    with SessionLocal() as session:
        content_service = ContentService(session)
        text = content_service.get_faq_text()

    await update.message.reply_text(
        text=text,
        reply_markup=MAIN_MENU_KEYBOARD,
    )


async def show_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    with SessionLocal() as session:
        content_service = ContentService(session)
        text = content_service.get_contacts_text()

    await update.message.reply_text(
        text=text,
        reply_markup=MAIN_MENU_KEYBOARD,
    )


def get_content_handlers() -> list[MessageHandler]:
    return [
        MessageHandler(filters.Regex("^🏠 Главное меню$"), show_main_menu),
        MessageHandler(filters.Regex("^🔥 Акции$"), show_promotions),
        MessageHandler(filters.Regex("^🏢 О нас$"), show_about),
        MessageHandler(filters.Regex("^❓ Частые вопросы$"), show_faq),
        MessageHandler(filters.Regex("^📞 Контакты$"), show_contacts),
    ]
