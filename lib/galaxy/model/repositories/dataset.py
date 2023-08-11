from galaxy.model import Dataset
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class DatasetRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, Dataset)
