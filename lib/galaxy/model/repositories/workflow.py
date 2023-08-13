from typing import (
    cast,
    Optional,
)

from galaxy.model import Workflow
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
