from galaxy.model import FormDefinition
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class FormDefinitionRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, FormDefinition)
