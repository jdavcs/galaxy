from typing import (
    cast,
    Optional,
)

from galaxy.model import InteractiveToolEntryPoint
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class InteractiveToolEntryPointRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or InteractiveToolEntryPoint
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> InteractiveToolEntryPoint:
        return cast(InteractiveToolEntryPoint, super().get(primary_key))
