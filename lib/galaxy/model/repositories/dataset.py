from sqlalchemy.orm import Session

from galaxy.model import Dataset
from galaxy.model.repositories import ModelRepository


class DatasetRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, Dataset)
