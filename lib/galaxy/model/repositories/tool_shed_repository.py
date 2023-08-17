from sqlalchemy import (
    and_,
    cast,
    Integer,
    select,
)

from galaxy.model.repositories import (
    ModelRepository,
    SessionType,
)
from galaxy.model.tool_shed_install import ToolShedRepository


class ToolShedRepositoryRepository(ModelRepository):
    def __init__(self, session: SessionType):
        super().__init__(session, ToolShedRepository)

    def get_filtered(self, name, owner, changeset, deleted, uninstalled):
        clause_list = []
        if name is not None:
            clause_list.append(ToolShedRepository.name == name)
        if owner is not None:
            clause_list.append(ToolShedRepository.owner == owner)
        if changeset is not None:
            clause_list.append(ToolShedRepository.changeset_revision == changeset)
        if deleted is not None:
            clause_list.append(ToolShedRepository.deleted == deleted)
        if uninstalled is not None:
            clause_list.append(ToolShedRepository.uninstalled == uninstalled)

        stmt = (
            select(ToolShedRepository)
            .order_by(ToolShedRepository.name)
            .order_by(cast(ToolShedRepository.ctx_rev, Integer).desc())
        )
        if len(clause_list) > 0:
            stmt = stmt.filter(and_(*clause_list))
        return self.session.scalars(stmt).all()  # type:ignore[union-attr]
