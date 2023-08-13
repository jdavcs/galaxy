from typing import (
    cast,
    Optional,
)

from galaxy.model import HistoryDatasetCollectionAssociation
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class HistoryDatasetCollectionAssociationRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or HistoryDatasetCollectionAssociation
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> HistoryDatasetCollectionAssociation:
        return cast(HistoryDatasetCollectionAssociation, super().get(primary_key))
