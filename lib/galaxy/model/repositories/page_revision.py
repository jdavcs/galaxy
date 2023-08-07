from sqlalchemy import select

from galaxy.model import PageRevision
from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)


class PageRevisionRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, PageRevision)

    def get_by_page(self, page_id: int):
        stmt = select(PageRevision).filter_by(page_id=page_id)
        return self.session.scalars(stmt).all()  # type:ignore[union-attr]
