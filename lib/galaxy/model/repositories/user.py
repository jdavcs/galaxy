from sqlalchemy import (
    false,
    func,
    select,
)

from galaxy.model import (
    User,
    UserRoleAssociation,
)


class UserRepository:

    def get_user_by_username(session, username):
        stmt = select(User).where(User.username == username).limit(1)
        return session.scalars(stmt).first()

    def get_user_by_email(session, email):
        stmt = select(User).where(User.email == email).limit(1)
        return session.scalars(stmt).first()

    def get_users_by_ids(session, user_ids):
        stmt = select(User).where(User.id.in_(user_ids))
        return session.scalars(stmt).all()

    def get_users_by_role(session, role):
        stmt = select(User).join(UserRoleAssociation).where(UserRoleAssociation.role == role)
        return session.scalars(stmt).all()

    def email_exists(session, email):
        stmt = select(User).where(func.lower(User.email) == email.lower()).limit(1)
        return bool(session.scalars(stmt).first())

    def get_deleted_users(session):
        stmt = select(User).where(User.deleted == false()).order_by(User.email)
        return session.scalars(stmt).all()

