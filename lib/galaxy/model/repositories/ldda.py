from typing import (
    cast,
    Optional,
)

from galaxy.model import LibraryDatasetDatasetAssociation
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


# Remove type:ignore annotations after LDDA is mapped declaratively.
class LibraryDatasetDatasetAssociationRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or LibraryDatasetDatasetAssociation  # type:ignore[assignment]
        super().__init__(session, model_class)  # type:ignore[arg-type]

    def get(self, primary_key: int) -> LibraryDatasetDatasetAssociation:  # type:ignore[override]
        return cast(LibraryDatasetDatasetAssociation, super().get(primary_key))
