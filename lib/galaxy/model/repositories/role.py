from sqlalchemy.orm import Session

from galaxy.model import Role
from galaxy.model.repositories import ModelRepository


class RoleRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, Role)
