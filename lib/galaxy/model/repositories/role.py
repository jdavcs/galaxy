from typing import (
    cast,
    Optional,
)

from galaxy.model import Role
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class RoleRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or Role
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> Role:
        return cast(Role, super().get(primary_key))
