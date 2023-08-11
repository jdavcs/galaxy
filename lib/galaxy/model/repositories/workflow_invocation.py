from galaxy.model import WorkflowInvocation
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class WorkflowInvocationRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, WorkflowInvocation)
