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