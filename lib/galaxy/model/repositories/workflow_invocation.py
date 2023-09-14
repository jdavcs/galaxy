from sqlalchemy.orm import Session

from galaxy.model import WorkflowInvocation
from galaxy.model.repositories import ModelRepository


class WorkflowInvocationRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, WorkflowInvocation)
