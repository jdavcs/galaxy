from galaxy.model import HistoryDatasetAssociation
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


# Remove type:ignore annotations after HDA is mapped declaratively.
class HistoryDatasetAssociationRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, HistoryDatasetAssociation)  # type:ignore[arg-type]
