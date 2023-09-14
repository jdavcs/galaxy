from sqlalchemy.orm import Session

from galaxy.model import LibraryDatasetDatasetAssociation
from galaxy.model.repositories import ModelRepository


# Remove type:ignore annotations after LDDA is mapped declaratively.
class LibraryDatasetDatasetAssociationRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, LibraryDatasetDatasetAssociation)  # type:ignore[arg-type]
