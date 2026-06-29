from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.promotion import Promotion


class PromotionRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_active(self) -> list[Promotion]:
        stmt = (
            select(Promotion)
            .where(Promotion.is_active.is_(True))
            .order_by(Promotion.created_at.desc())
        )
        return list(self.session.scalars(stmt).all())