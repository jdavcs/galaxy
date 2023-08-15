from typing import (
    cast,
    List,
    Optional,
)

from sqlalchemy import select

from galaxy.model import HistoryDatasetAssociation
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


# Remove type:ignore annotations after HDA is mapped declaratively.
class HistoryDatasetAssociationRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or HistoryDatasetAssociation  # type:ignore[assignment]
        super().__init__(session, model_class)  # type:ignore[arg-type]

    def get(self, primary_key: int) -> HistoryDatasetAssociation:  # type:ignore[override]
        return cast(HistoryDatasetAssociation, super().get(primary_key))

    def get_with_filter_order_by_hid(self, **kwd) -> List:
        # type-ignore/SessionlessContext
        stmt = (
            select(self.model_class).filter_by(**kwd).order_by(self.model_class.hid.desc())  # type:ignore[attr-defined]
        )
        return self.session.scalars(stmt).all()  # type:ignore[union-attr]
