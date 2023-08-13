from typing import (
    cast,
    Optional,
)

from galaxy.model import DatasetCollectionElement
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class DatasetCollectionElementRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or DatasetCollectionElement
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> DatasetCollectionElement:
        return cast(DatasetCollectionElement, super().get(primary_key))
