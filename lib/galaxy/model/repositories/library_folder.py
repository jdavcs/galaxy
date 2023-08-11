from galaxy.model import LibraryFolder
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class LibraryFolderRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, LibraryFolder)
