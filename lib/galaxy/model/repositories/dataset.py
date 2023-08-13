from typing import (
    cast,
    Optional,
)

from galaxy.model import Dataset
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class DatasetRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or Dataset
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> Dataset:
        return cast(Dataset, super().get(primary_key))
