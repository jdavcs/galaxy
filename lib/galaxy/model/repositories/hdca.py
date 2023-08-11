from galaxy.model import HistoryDatasetCollectionAssociation
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class HistoryDatasetCollectionAssociationRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, HistoryDatasetCollectionAssociation)
