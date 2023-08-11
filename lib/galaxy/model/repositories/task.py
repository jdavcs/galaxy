from galaxy.model import Task
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class TaskRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, Task)
