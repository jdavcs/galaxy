from typing import (
    cast,
    Optional,
)

from galaxy.model import Task
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class TaskRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or Task
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> Task:
        return cast(Task, super().get(primary_key))
