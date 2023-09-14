from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from galaxy.model import Base

MappedType = Base


class ModelRepository:
    # self.session can be an instance of galaxy.model.store.SessionlessContext,
    # which implements a very small subset of SQLAlchemy's Session attributes.
    # We type-ignore instead of a typecheck+assert for the sake of performance.
    def __init__(self, session: Session, model_class: MappedType):
        self.session = session
        self.model_class = model_class

    def get(self, primary_key: Any):
        # type-ignore/SessionlessContext: expects model_class to have an id attribute.
        return self.session.get(self.model_class, primary_key)  # type:ignore[arg-type]

    def get_all(self):
        # type-ignore/SessionlessContext
        return self.session.scalars(select(self.model_class)).all()  # type:ignore[union-attr]
