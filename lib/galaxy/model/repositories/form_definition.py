from typing import (
    cast,
    Optional,
)

from galaxy.model import FormDefinition
from galaxy.model.repositories import (
    BaseRepository,
    MappedType,
    SessionType,
)


class FormDefinitionRepository(BaseRepository):
    def __init__(self, session: SessionType, model_class: Optional[MappedType] = None):
        model_class = model_class or FormDefinition
        super().__init__(session, model_class)

    def get(self, primary_key: int) -> FormDefinition:
        return cast(FormDefinition, super().get(primary_key))
