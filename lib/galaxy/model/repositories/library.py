from sqlalchemy.orm import Session

from galaxy.model import Library
from galaxy.model.repositories import ModelRepository


class LibraryRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, Library)
