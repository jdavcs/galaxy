from sqlalchemy.orm import Session

from galaxy.model import StoredWorkflow
from galaxy.model.repositories import ModelRepository


class StoredWorkflowRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, StoredWorkflow)
