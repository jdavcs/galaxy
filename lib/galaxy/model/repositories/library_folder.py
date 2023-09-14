from sqlalchemy.orm import Session

from galaxy.model import LibraryFolder
from galaxy.model.repositories import ModelRepository


class LibraryFolderRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, LibraryFolder)
