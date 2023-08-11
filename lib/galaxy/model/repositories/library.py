from galaxy.model import Library
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class LibraryRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, Library)
