from galaxy.model import InteractiveToolEntryPoint
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class InteractiveToolEntryPointRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, InteractiveToolEntryPoint)
