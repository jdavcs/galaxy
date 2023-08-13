from typing import (
    cast,
    Optional,
)

from galaxy.model import StoredWorkflow
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class StoredWorkflowRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or StoredWorkflow
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> StoredWorkflow:
        return cast(StoredWorkflow, super().get(primary_key))
