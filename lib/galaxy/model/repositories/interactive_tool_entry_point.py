from sqlalchemy.orm import Session

from galaxy.model import InteractiveToolEntryPoint
from galaxy.model.repositories import ModelRepository


class InteractiveToolEntryPointRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, InteractiveToolEntryPoint)
