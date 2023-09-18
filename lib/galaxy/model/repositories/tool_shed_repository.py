from sqlalchemy import (
    cast,
    Integer,
    select,
)
from sqlalchemy.orm import Session

from galaxy.model.repositories import ModelRepository
from galaxy.model.tool_shed_install import ToolShedRepository


class ToolShedRepositoryRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, ToolShedRepository)

    def get_filtered(self, **kwd):
        stmt = select(ToolShedRepository)
        for key, value in kwd.items():
            if value is not None:
                column = ToolShedRepository.table.c[key]
                stmt = stmt.filter(column == value)
        stmt = stmt.order_by(ToolShedRepository.name).order_by(cast(ToolShedRepository.ctx_rev, Integer).desc())
        return self.session.scalars(stmt).all()
