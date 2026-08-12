import re

from sqlalchemy.orm import Session

from app.errors import ValidationError
from app.models.application import Application
from app.repositories.application import ApplicationRepository


class ApplicationService:
    field_order = ("name", "phone", "city", "company", "email", "comment")
    required_fields = {"name", "phone"}
    optional_fields = {"city", "company", "email", "comment"}

    field_prompts = {
        "name": "Введите ваше имя.",
        "phone": "Введите телефон для связи.",
        "city": "Введите город или нажмите «Пропустить».",
        "company": "Введите название компании или нажмите «Пропустить».",
        "email": "Введите email или нажмите «Пропустить».",
        "comment": "Добавьте комментарий или нажмите «Пропустить».",
    }

    def __init__(self, session: Session):
        self.repository = ApplicationRepository(session)

    def get_start_text(self) -> str:
        return (
            "Сейчас я задам несколько вопросов для заявки.\n\n"
            "Обязательные поля: имя и телефон.\n"
            "Остальные поля можно пропустить."
        )

    def get_first_field(self) -> str:
        return self.field_order[0]

    def get_field_prompt(self, field: str) -> str:
        return self.field_prompts[field]

    def validate_field(self, field: str, value: str) -> str:
        value = value.strip()

        if field in self.required_fields and not value:
            raise ValidationError("Это поле обязательно. Введите значение.")

        if field == "phone":
            self._validate_phone(value)

        if field == "email" and value:
            self._validate_email(value)

        return value

    def can_skip_field(self, field: str) -> bool:
        return field in self.optional_fields

    def get_next_field(self, current_field: str) -> str | None:
        current_index = self.field_order.index(current_field)
        next_index = current_index + 1

        if next_index >= len(self.field_order):
            return None

        return self.field_order[next_index]

    def prepare_application_data(self, form_data: dict) -> dict:
        return {
            "name": form_data["name"],
            "phone": form_data["phone"],
            "city": form_data.get("city"),
            "company": form_data.get("company"),
            "email": form_data.get("email"),
            "comment": form_data.get("comment"),
        }

    def create_application(self, user_id: int, form_data: dict) -> Application:
        application_data = self.prepare_application_data(form_data)

        return self.repository.create(
            user_id=user_id,
            **application_data,
        )

    def mark_notification_sent(self, application: Application) -> Application:
        return self.repository.update_notification_status(
            application=application,
            notification_status="sent",
        )

    def mark_notification_failed(self, application: Application) -> Application:
        return self.repository.update_notification_status(
            application=application,
            notification_status="failed",
        )

    def get_manager_notification_text(self, application: Application) -> str:
        return (
            "Новая заявка\n\n"
            f"Имя: {application.name}\n"
            f"Телефон: {application.phone}\n"
            f"Город: {application.city or 'не указан'}\n"
            f"Компания: {application.company or 'не указана'}\n"
            f"Email: {application.email or 'не указан'}\n"
            f"Комментарий: {application.comment or 'не указан'}"
        )

    def get_success_text(self) -> str:
        return (
            "Заявка принята. "
            "Менеджер свяжется с вами в ближайшее время."
        )

    def _validate_phone(self, phone: str) -> None:
        digits = re.sub(r"\D", "", phone)

        if len(digits) < 10 or len(digits) > 15:
            raise ValidationError(
                "Похоже, телефон указан некорректно. Введите номер ещё раз."
            )

    def _validate_email(self, email: str) -> None:
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            raise ValidationError(
                "Похоже, почта указана некорректно. "
                "Введите её ещё раз или нажмите «Пропустить»."
            )
