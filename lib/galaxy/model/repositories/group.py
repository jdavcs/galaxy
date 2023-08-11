from galaxy.model import Group
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class GroupRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, Group)
