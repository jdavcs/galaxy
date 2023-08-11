from typing import (
    cast,
    Optional,
)

from galaxy.model import Job
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class JobRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or Job
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> Job:
        return cast(Job, super().get(primary_key))
