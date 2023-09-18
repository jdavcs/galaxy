from sqlalchemy import (
    select,
    update,
)
from sqlalchemy.orm import Session

from galaxy.model import APIKeys
from galaxy.model.repositories import ModelRepository


# Remove type:ignore annotations after LDDA is mapped declaratively.
class APIKeysRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, APIKeys)  # type:ignore[arg-type]

    def get_api_key(self, user_id: int):
        stmt = select(APIKeys).filter_by(user_id=user_id, deleted=False).order_by(APIKeys.create_time.desc()).limit(1)
        return self.session.scalars(stmt).first()

    def mark_all_as_deleted(self, user_id: int):
        stmt = (
            update(APIKeys)
            .where(APIKeys.user_id == user_id)
            .where(APIKeys.deleted == False)  # noqa: E712
            .values(deleted=True)
            .execution_options(synchronize_session="evaluate")
        )
        return self.session.execute(stmt)
