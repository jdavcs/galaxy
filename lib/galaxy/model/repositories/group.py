from sqlalchemy import select
from sqlalchemy.orm import Session

from galaxy.model import Group
from galaxy.model.repositories import ModelRepository


class GroupRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, Group)

    def get_by_name(self, name: str):
        stmt = select(Group).filter(Group.name == name).limit(1)
        return self.session.scalars(stmt).first()  # type:ignore[union-attr]
