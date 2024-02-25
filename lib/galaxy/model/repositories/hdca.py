from sqlalchemy import select

from galaxy.model import HistoryDatasetCollectionAssociation


class HDCARepository:

    def get_hdca_by_name(session, name):
        stmt = (
            select(HistoryDatasetCollectionAssociation).where(HistoryDatasetCollectionAssociation.name == name).limit(1)
        )
        return session.scalars(stmt).first()
