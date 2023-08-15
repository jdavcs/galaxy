from typing import (
    cast,
    Optional,
)

from galaxy.model import User
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class UserRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or User
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> User:
        return cast(User, super().get(primary_key))

    def get_foo(self):
        stmt = select(User).filter(User.username == username)
        return self.session.execute(stmt).scalar_one()
