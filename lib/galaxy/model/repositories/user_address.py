from sqlalchemy.orm import Session

from galaxy.model import UserAddress
from galaxy.model.repositories import ModelRepository


class UserAddressRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, UserAddress)
