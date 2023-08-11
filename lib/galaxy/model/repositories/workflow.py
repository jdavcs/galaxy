from sqlalchemy import (
    func,
    select,
)

from galaxy.model import (
    StoredWorkflowUserShareAssociation,
    Workflow,
)
from galaxy.model.repositories import (
    MappedType,
    ModelRepository,
    SessionType,
)


class WorkflowRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, Workflow)

    def count_stored_workflow_user_assocs(self, user: MappedType, stored_workflow: MappedType) -> int:
        # type-ignore/SessionlessContext
        stmt = select(StoredWorkflowUserShareAssociation).filter_by(user=user, stored_workflow=stored_workflow)
        stmt = select(func.count()).select_from(stmt)
        return self.session.scalar(stmt)  # type:ignore[union-attr]
