from sqlalchemy import select

from galaxy.model import User
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class UserRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, User)

    def get_by_email(self, email: str):
        stmt = select(User).filter(User.email == email).limit(1)
        return self.session.scalars(stmt).first()  # type:ignore[union-attr]


def get_user_by_username(session: SessionType, user_class, username: str):
    """Get a user from the database by username."""
    # This may be called from the tool_shed app, which has a different
    # definition of the User mapped class. Therefore, we must pass the User
    # class as an argument instead of importing from galaxy.model.
    stmt = select(user_class).filter(user_class.username == username)
    return session.execute(stmt).scalar_one()  # type:ignore[union-attr]
