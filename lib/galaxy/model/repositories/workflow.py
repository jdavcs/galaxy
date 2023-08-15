from typing import (
    cast,
    Optional,
)

from sqlalchemy import (
    func,
    select,
)

from galaxy.model import (
    StoredWorkflowUserShareAssociation,
    Workflow,
)
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class WorkflowRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or Workflow
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> Workflow:
        return cast(Workflow, super().get(primary_key))

    def count_stored_workflow_user_assocs(self, user: MappedType, stored_workflow: MappedType) -> int:
        # type-ignore/SessionlessContext
        stmt = select(StoredWorkflowUserShareAssociation).filter_by(user=user, stored_workflow=stored_workflow)
        stmt = select(func.count()).select_from(stmt)
        return self.session.scalar(stmt)  # type:ignore[union-attr]
