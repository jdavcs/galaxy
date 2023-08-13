from typing import (
    cast,
    Optional,
)

from galaxy.model import WorkflowInvocation
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class WorkflowInvocationRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or WorkflowInvocation
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> WorkflowInvocation:
        return cast(WorkflowInvocation, super().get(primary_key))
