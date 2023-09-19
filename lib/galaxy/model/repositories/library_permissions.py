from sqlalchemy.orm import Session

from galaxy.model import LibraryPermissions
from galaxy.model.repositories import ModelRepository


class LibraryPermissionsRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, LibraryPerission)

    def get_ids_by_action(self, library_access_action):
        stmt = select(LibraryPermissions).where(LibraryPermissions.action == library_access_action).distinct()
        return self.session.scalars(stmt)

    def get_permissions_by_role_ids(self, role_ids):
        stmt = select(LibraryPermissions).where(LibraryPermissions.role_id.in_(role_ids))
        return self.session.scalars(stmt).all()
