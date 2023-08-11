from galaxy.model import LibraryDatasetDatasetAssociation
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


# Remove type:ignore annotations after LDDA is mapped declaratively.
class LibraryDatasetDatasetAssociationRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, LibraryDatasetDatasetAssociation)  # type:ignore[arg-type]
