from typing import (
    cast,
    Optional,
)

from galaxy.model import PageRevision
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class PageRevisionRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or PageRevision
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> PageRevision:
        return cast(PageRevision, super().get(primary_key))
