from sqlalchemy import select
from sqlalchemy.orm import Session

from galaxy.model import Role
from galaxy.model.repositories import ModelRepository


class RoleRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, Role)

    def get_roles_by_ids(self, role_ids):
        stmt = select(Role).where(Role.id.in_(role_ids))
        return self.session.scalars(stmt).all()
