from galaxy.model import Job
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class JobRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, Job)
