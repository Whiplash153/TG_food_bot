from sqlalchemy.orm import Session

from app.models.promotion import Promotion
from app.repositories.promotion import PromotionRepository


class ContentService:
    def __init__(self, session: Session):
        self.promotion_repository = PromotionRepository(session)

    def get_main_menu_text(self) -> str:
        return (
            "Здравствуйте! Я помогу узнать об актуальных предложениях "
            "и оставить заявку для связи с менеджером."
        )

    def get_active_promotions(self) -> list[Promotion]:
        return self.promotion_repository.get_active()

    def format_promotions(self, promotions: list[Promotion]) -> str:
        if not promotions:
            return self.get_no_promotions_text()

        promotion_lines = []
        for promotion in promotions:
            promotion_lines.append(
                f"🔥 {promotion.title}\n{promotion.description}"
            )

        return "\n\n".join(promotion_lines)

    def get_no_promotions_text(self) -> str:
        return (
            "Актуальных акций сейчас нет. "
            "Вы можете оставить заявку, и менеджер свяжется с вами."
        )

    def get_about_text(self) -> str:
        return (
            "Мы поставляем продукты для бизнеса и помогаем подобрать "
            "подходящие предложения под ваши задачи."
        )

    def get_faq_text(self) -> str:
        return (
            "Частые вопросы:\n\n"
            "1. Можно ли оставить заявку через бот?\n"
            "Да, менеджер получит заявку и свяжется с вами.\n\n"
            "2. Нужно ли регистрироваться?\n"
            "Нет, достаточно заполнить форму заявки.\n\n"
            "3. Где смотреть актуальные предложения?\n"
            "В разделе «Акции»."
        )

    def get_contacts_text(self) -> str:
        return (
            "Контакты:\n\n"
            "Телефон: будет добавлен\n"
            "Почта: будет добавлена\n"
            "Адрес: будет добавлен\n"
            "График работы: будет добавлен"
        )

    def get_unknown_text(self) -> str:
        return "Пожалуйста, используйте кнопки текущего раздела."