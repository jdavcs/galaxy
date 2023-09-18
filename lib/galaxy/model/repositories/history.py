from sqlalchemy.orm import Session

from galaxy.model import History
from galaxy.model.repositories import ModelRepository


# Remove type:ignore annotations after LDDA is mapped declaratively.
class HistoryRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, History)  # type:ignore[arg-type]
