from sqlalchemy.orm import Session

from galaxy.model import Visualization
from galaxy.model.repositories import ModelRepository


class VisualizationRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, Visualization)
