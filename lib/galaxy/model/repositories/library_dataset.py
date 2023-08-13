from typing import (
    cast,
    Optional,
)

from galaxy.model import LibraryDataset
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class LibraryDatasetRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or LibraryDataset
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> LibraryDataset:
        return cast(LibraryDataset, super().get(primary_key))
