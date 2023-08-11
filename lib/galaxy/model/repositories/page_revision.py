from galaxy.model import PageRevision
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class PageRevisionRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, PageRevision)
