from sqlalchemy.orm import Session

from galaxy.model import DatasetCollectionElement
from galaxy.model.repositories import ModelRepository


class DatasetCollectionElementRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, DatasetCollectionElement)
