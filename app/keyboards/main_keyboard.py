from telegram import KeyboardButton, ReplyKeyboardMarkup


MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("🔥 Акции"),
            KeyboardButton("🏢 О нас"),
        ],
        [
            KeyboardButton("❓ Частые вопросы"),
            KeyboardButton("📞 Контакты"),
        ],
        [
            KeyboardButton("📝 Оставить заявку"),
        ],
    ],
    resize_keyboard=True,
)


BACK_TO_MENU_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("⬅ Назад"),
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