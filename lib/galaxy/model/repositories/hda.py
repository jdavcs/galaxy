from sqlalchemy import select
from sqlalchemy.orm import Session

from galaxy.model import HistoryDatasetAssociation
from galaxy.model.repositories import ModelRepository


# Remove type:ignore annotations after HDA is mapped declaratively.
class HistoryDatasetAssociationRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, HistoryDatasetAssociation)  # type:ignore[arg-type]

    def get_fasta_hdas_by_history(self, history_id: int):
        # type-ignore/SessionlessContext
        stmt = (
            select(HistoryDatasetAssociation)
            .filter_by(history_id=history_id, extension="fasta", deleted=False)
            .order_by(HistoryDatasetAssociation.hid.desc())  # type:ignore[attr-defined]
        )
        return self.session.scalars(stmt).all()  # type:ignore[union-attr]

    def get_len_files_by_history(self, history_id: int):
        stmt = select(HistoryDatasetAssociation).filter_by(history_id=history_id, extension="len", deleted=False)
        return self.session.scalars(stmt)
