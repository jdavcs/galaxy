from typing import (
    cast,
    Optional,
)

from galaxy.model import Visualization
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class VisualizationRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or Visualization
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> Visualization:
        return cast(Visualization, super().get(primary_key))
