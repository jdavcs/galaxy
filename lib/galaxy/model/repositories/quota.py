from sqlalchemy import (
    false,
    select,
    true,
)
from sqlalchemy.orm import Session

from galaxy.model import Quota
from galaxy.model.repositories import ModelRepository


class QuotaRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, Quota)

    def get_deleted(self, deleted: bool = True):
        # type-ignore/SessionlessContext
        is_deleted = true()
        if not deleted:
            is_deleted = false()
        stmt = select(Quota).filter(Quota.deleted == is_deleted)  # type:ignore[attr-defined]
        return self.session.scalars(stmt).all()  # type:ignore[union-attr]
