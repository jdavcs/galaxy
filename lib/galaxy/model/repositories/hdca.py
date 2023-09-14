from sqlalchemy.orm import Session

from galaxy.model import HistoryDatasetCollectionAssociation
from galaxy.model.repositories import ModelRepository


class HistoryDatasetCollectionAssociationRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, HistoryDatasetCollectionAssociation)
