from galaxy.model import Role
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class RoleRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, Role)
