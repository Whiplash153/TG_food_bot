from datetime import UTC, datetime, time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.application import Application


class ApplicationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        user_id: int,
        name: str,
        phone: str,
        city: str | None,
        company: str | None,
        email: str | None,
        comment: str | None,
    ) -> Application:
        application = Application(
            user_id=user_id,
            name=name,
            phone=phone,
            city=city,
            company=company,
            email=email,
            comment=comment,
        )
        self.session.add(application)
        self.session.commit()
        self.session.refresh(application)
        return application

    def update_notification_status(
        self,
        application: Application,
        notification_status: str,
    ) -> Application:
        application.notification_status = notification_status

        self.session.commit()
        self.session.refresh(application)
        return application

    def get_today(self) -> list[Application]:
        today = datetime.now(UTC).date()
        start_of_day = datetime.combine(today, time.min, tzinfo=UTC)
        end_of_day = datetime.combine(today, time.max, tzinfo=UTC)

        stmt = (
            select(Application)
            .where(Application.created_at >= start_of_day)
            .where(Application.created_at <= end_of_day)
            .order_by(Application.created_at.desc())
        )

        return list(self.session.scalars(stmt).all())