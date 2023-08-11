from galaxy.model import Visualization
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class VisualizationRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, Visualization)
