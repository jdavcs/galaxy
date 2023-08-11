from galaxy.model import UserAddress
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class UserAddressRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, UserAddress)
