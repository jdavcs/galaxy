from sqlalchemy import select

from galaxy.model import User
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class UserRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, User)


# The get_user_by_email and get_user_by_username functions may be called from
# the tool_shed app, which has its own User model, which is different from
# galaxy.model.User. In that case, the tool_shed user model should be passed as
# the model_class argument.
def get_user_by_email(session, email: str, model_class=User):
    stmt = select(model_class).filter(model_class.email == email).limit(1)
    return session.scalars(stmt).first()


def get_user_by_username(session, username: str, model_class=User):
    stmt = select(model_class).filter(model_class.username == username).limit(1)
    return session.scalars(stmt).first()
