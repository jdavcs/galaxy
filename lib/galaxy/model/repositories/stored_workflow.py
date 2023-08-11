from galaxy.model import StoredWorkflow
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class StoredWorkflowRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, StoredWorkflow)
