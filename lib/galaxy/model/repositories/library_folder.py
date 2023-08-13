from typing import (
    cast,
    Optional,
)

from galaxy.model import LibraryFolder
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class LibraryFolderRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or LibraryFolder
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> LibraryFolder:
        return cast(LibraryFolder, super().get(primary_key))
