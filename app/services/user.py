from sqlalchemy.orm import Session
from telegram import User as TelegramUser

from app.models.user import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, session: Session):
        self.repository = UserRepository(session)

    def create_or_update_user(self, telegram_user: TelegramUser) -> User:
        user = self.repository.get_by_telegram_id(telegram_user.id)

        if user is None:
            return self.repository.create(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
                language_code=telegram_user.language_code,
            )

        return self.repository.update(
            user=user,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            language_code=telegram_user.language_code,
        )

    def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return self.repository.get_by_telegram_id(telegram_id)