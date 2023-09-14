from sqlalchemy.orm import Session

from galaxy.model import FormDefinition
from galaxy.model.repositories import ModelRepository


class FormDefinitionRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, FormDefinition)
