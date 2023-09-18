from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from galaxy.model import Base

MappedType = Base


class ModelRepository:
    def __init__(self, session: Session, model_class: MappedType):
        self.session = session
        self.model_class = model_class

    def get(self, primary_key: Any):
        return self.session.get(self.model_class, primary_key)

    def get_all(self):
        return self.session.scalars(select(self.model_class)).all()
