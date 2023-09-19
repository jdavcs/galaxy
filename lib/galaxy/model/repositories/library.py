from sqlalchemy.orm import Session

from galaxy.model import Library
from galaxy.model.repositories import ModelRepository


class LibraryRepository(ModelRepository):
    def __init__(self, session: Session):
        super().__init__(session, Library)

    def get_not_deleted_by_name(self, name):
        stmt = select(Library).where(Library.deleted == false()).where(Library.name == name)
        return self.session.scalars(stmt)


    def get_list(self):
        stmt = select(Library)

        if is_admin:
            if deleted is None:
                pass
            elif deleted:
                stmt = stmt.where(Library.deleted == true())
            else:
                stmt = stmt.where(Library.deleted == false())
        else:
            if deleted:
                raise exceptions.AdminRequiredException()
            else:
                stmt = stmt.where(Library.deleted == false())
