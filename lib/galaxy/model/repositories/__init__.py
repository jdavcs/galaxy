from typing import (
    Any,
    List,
    Union,
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from galaxy.model import Base
from galaxy.model.store import SessionlessContext

SessionType = Union[Session, SessionlessContext]
MappedType = Base


class BaseRepository:
    # self.session can be an instance of galaxy.model.store.SessionlessContext,
    # which implements a very small subset of SQLAlchemy's Session attributes.
    # We type-ignore instead of a typecheck+assert for the sake of performance.
    def __init__(self, session: SessionType, model_class: MappedType):
        self.session = session
        self.model_class = model_class

    def get(self, primary_key: Any) -> MappedType:
        # type-ignore/SessionlessContext: expects model_class to have an id attribute.
        return self.session.get(self.model_class, primary_key)  # type:ignore[arg-type]

    def get_all(self) -> List:
        # type-ignore/SessionlessContext
        return self.session.scalars(select(self.model_class)).all()  # type:ignore[union-attr]

    def get_with_filter(self, **kwd) -> List:
        # type-ignore/SessionlessContext
        stmt = select(self.model_class).filter_by(**kwd)
        return self.session.scalars(stmt).all()  # type:ignore[union-attr]
