from telegram import KeyboardButton, ReplyKeyboardMarkup


MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("🔥 Акции"),
            KeyboardButton("🏢 О компании"),
        ],
        [
            KeyboardButton("❓ Частые вопросы"),
            KeyboardButton("📞 Контакты"),
        ],
        [
            KeyboardButton("📝 Оставить заявку"),
        ],
        [
            KeyboardButton("🏠 Главное меню"),
        ],
    ],
    resize_keyboard=True,
)


APPLICATION_FORM_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Пропустить"),
        ],
        [
            KeyboardButton("Отменить заявку"),
            KeyboardButton("🏠 Главное меню"),
        ],
    ],
    resize_keyboard=True,
)
