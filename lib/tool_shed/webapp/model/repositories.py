from sqlalchemy import select
from tool_shed.webapp.model import User


class UserRepository:

    def get_by_username(self, session, username: str):
        stmt = select(User).filter(User.username == username).limit(1)
        return session.scalars(stmt).first()
