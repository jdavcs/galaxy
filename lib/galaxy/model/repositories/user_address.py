from typing import (
    cast,
    Optional,
)

from galaxy.model import UserAddress
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class UserAddressRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or UserAddress
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> UserAddress:
        return cast(UserAddress, super().get(primary_key))
