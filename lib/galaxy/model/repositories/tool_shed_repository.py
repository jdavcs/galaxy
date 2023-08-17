from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)
from galaxy.model.tool_shed_install import ToolShedRepository


class ToolShedRepositoryRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, ToolShedRepository)
