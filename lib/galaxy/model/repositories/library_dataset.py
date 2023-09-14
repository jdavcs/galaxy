from sqlalchemy.orm import Session

from galaxy.model import LibraryDataset
from galaxy.model.repositories import ModelRepository


class LibraryDatasetRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, LibraryDataset)
