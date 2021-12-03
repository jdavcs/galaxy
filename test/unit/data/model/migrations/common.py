import logging
import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.sql.compiler import IdentifierPreparer

from galaxy.model.database_utils import create_database


log = logging.getLogger(__name__)


def get_connection_url():
    """only postgres."""  # TODO edit comment
    # TODO remove this
    #return 'postgresql://galaxy:42@localhost:5432/alembic_5?client_encoding=utf8'
    url = os.environ.get('GALAXY_TEST_DBURI')
    log.debug(f'\nCONN_URL: {url}')
    print(f'\nCONN_URL: {url}')
    return url


@contextmanager
def disposing_engine(url):
    engine = create_engine(url)
    try:
        yield engine
    finally:
        engine.dispose()


@contextmanager  # TODO consider this
def create_and_drop_database(db_url):
    """Provides cleanup for postgres db; sqlite is removed by tempfile"""  # TODO edit comment
    try:
        create_database(db_url)
        yield
    finally:
        pass
        log.debug(f'\ndropping: {db_url}')
        print(f'\ndropping: {db_url}')
        if _is_postgres(db_url):
            url = make_url(db_url)
            _drop_postgres_database(url.database)


def _is_postgres(db_url):
    return db_url.startswith('postgres')


def _drop_postgres_database(database):
    connection_url = get_connection_url()
    log.debug(f'\ncreating engine to drop using conn: {connection_url}')
    print(f'\ncreating engine to drop using conn: {connection_url}')
    engine = create_engine(connection_url, isolation_level='AUTOCOMMIT')
    preparer = IdentifierPreparer(engine.dialect)
    database = preparer.quote(database)
    #stmt = f'DROP DATABASE IF EXISTS {database}'
    stmt = f'DROP DATABASE {database}'
    log.debug(f'\ndropping stmt: {stmt}')
    print(f'\ndropping stmt: {stmt}')

    with engine.connect() as conn:     # TODO this causes an error remotely. why?
        conn.execute(stmt)
    engine.dispose()
