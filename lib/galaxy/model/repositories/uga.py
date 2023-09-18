from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from galaxy.model import UserGroupAssociation
from galaxy.model.repositories import ModelRepository


class UserGroupAssociationRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, UserGroupAssociation)

    def get_group_user(self, user, group) -> Optional[UserGroupAssociation]:
        stmt = (
            select(UserGroupAssociation)
            .where(UserGroupAssociation.user == user)
            .where(UserGroupAssociation.group == group)
        )
        return self.session.execute(stmt).scalar_one_or_none()
