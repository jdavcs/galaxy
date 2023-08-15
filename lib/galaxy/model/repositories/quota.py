from typing import (
    cast,
    List,
    Optional,
)

from sqlalchemy import (
    false,
    select,
    true,
)

from galaxy.model import Quota
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class QuotaRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or Quota
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> Quota:
        return cast(Quota, super().get(primary_key))

    def get_deleted(self, deleted: bool = True) -> List:
        # type-ignore/SessionlessContext
        if deleted:
            is_deleted = true()
        else:
            is_deleted = false()
        stmt = select(self.model_class).filter(self.model_class.deleted == is_deleted)  # type:ignore[attr-defined]
        return self.session.scalars(stmt).all()  # type:ignore[union-attr]
