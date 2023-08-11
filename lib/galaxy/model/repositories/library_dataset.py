from galaxy.model import LibraryDataset
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class LibraryDatasetRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, LibraryDataset)
