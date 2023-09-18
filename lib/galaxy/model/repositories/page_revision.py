from sqlalchemy import select
from sqlalchemy.orm import Session

from galaxy.model import PageRevision
from galaxy.model.repositories import ModelRepository


class PageRevisionRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, PageRevision)

    def get_by_page(self, page_id: int):
        stmt = select(PageRevision).filter_by(page_id=page_id)
        return self.session.scalars(stmt).all()
