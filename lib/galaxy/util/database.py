import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.compiler import IdentifierPreparer
from sqlalchemy.engine import make_url


def is_postgresql(db_url):
    return db_url.startswith('postgresql')


def database_exists(db_url, database):
    """Check if database exists; connect with db_url."""

    if is_postgresql(db_url):
        engine = create_engine(db_url)
        stmt = text('SELECT 1 FROM pg_database WHERE datname=:database')
        stmt = stmt.bindparams(database=database)
        with engine.connect() as conn:
            exists = bool(conn.scalar(stmt))
        engine.dispose()   
    else:
        # TODO do not assume sqlite: add error handling for invalid db url
        url = make_url(db_url)
        try:
            sqlite3.connect(f'file:{url.database}?mode=ro', uri=True)
            exists = True
        except sqlite3.OperationalError:
            exists = False

    return exists


def create_database(db_url, database, encoding='utf8', template=None):
    """Create database; connect with db_url."""

    if is_postgresql(db_url):
        engine = create_engine(db_url)
        preparer = IdentifierPreparer(engine.dialect)

        template = template or 'template1'
        database, template = preparer.quote(database), preparer.quote(template)
        stmt = f"CREATE DATABASE {database} ENCODING '{encoding}' TEMPLATE {template}"

        with engine.connect().execution_options(isolation_level='AUTOCOMMIT') as conn:
            conn.execute(stmt)
        engine.dispose()   
    else:
        url = make_url(db_url)
        try:
            sqlite3.connect(f'file:{url.database}', uri=True)
        except sqlite3.OperationalError:
            pass


