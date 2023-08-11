from galaxy.model import DatasetCollectionElement
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class DatasetCollectionElementRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, DatasetCollectionElement)
