from typing import (
    cast,
    Optional,
)

from galaxy.model import Library
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class LibraryRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or Library
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> Library:
        return cast(Library, super().get(primary_key))
