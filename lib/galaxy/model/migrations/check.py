import logging 

from sqlalchemy_utils import (
    create_database, 
    database_exists,
)

from .utils import DBManager


log = logging.getLogger(__name__)


# TODO: move these to exceptions?
class NoMigrateVersioningError(Exception):
    def __init__(self):
        super().__init__('not alembic, not migrate: upgrade manually')

class NoAlembicVersioningError(Exception):
    def __init__(self):
        super().__init__('not alembic, migrate: run migrate+alembic script')

class DBOutdatedError(Exception):
    def __init__(self):
        super().__init__('database is outdated: run alembic script')


def run(url, metadata, alembic_dir=None, auto_migrate=False): # TODO no args; mock in tests.

    if not database_exists(url):
        create_galaxy_database(url)

    dbm = DBManager(url, metadata, alembic_dir)

    if not dbm.is_initialized():
        dbm.initialize_schema()
        dbm.initialize_alembic()
        return

    if not dbm.is_alembic_versioned():
        if not dbm.is_migrate_versioned():
            raise NoMigrateVersioningError()
        else:
            if auto_migrate: # TODO
                print('TODO: run m+a scripts')
                #migrate_upgrade()
                #init_alembic()
                #alembic_upgrade()
                return
            raise NoAlembicVersioningError()

    if not dbm.is_current():
   #     if auto_migrate: # TODO
   #         alembic_upgrade()
   #         return
        raise DBOutdatedError()

    log.info('Database is up-to-date')
    # and we're done!



def create_galaxy_database(url):
    log.info('Creating database')
    create_database(url)
    assert database_exists(url)
