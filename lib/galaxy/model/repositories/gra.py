from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from galaxy.model import GroupRoleAssociation
from galaxy.model.repositories import ModelRepository


class GroupRoleAssociationRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, GroupRoleAssociation)

    def get_group_role(self, group, role) -> Optional[GroupRoleAssociation]:
        stmt = (
            select(GroupRoleAssociation)
            .where(GroupRoleAssociation.group == group)
            .where(GroupRoleAssociation.role == role)
        )
        return self.session.execute(stmt).scalar_one_or_none()
