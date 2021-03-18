import os
import pytest
import tempfile
import uuid

from galaxy.util.database import database_exists, create_database


# GALAXY_TEST_CONNECT_POSTGRES_URI='postgresql://postgres@localhost:5432/postgres' pytest test/unit/util/test_database.py
skip_if_not_postgres_uri = pytest.mark.skipif(
    not os.environ.get('GALAXY_TEST_CONNECT_POSTGRES_URI'),
    reason="GALAXY_TEST_CONNECT_POSTGRES_URI not set"
)


@pytest.fixture
def database_name():
    return f'galaxytest_{uuid.uuid4().hex}'


@pytest.fixture
def postgres_url():
    return os.environ.get('GALAXY_TEST_CONNECT_POSTGRES_URI')


@skip_if_not_postgres_uri
def test_postgres_database_does_not_exist(database_name, postgres_url):
    assert not database_exists(postgres_url, database_name)


@skip_if_not_postgres_uri
def test_postgres_create_database(database_name, postgres_url):
    assert not database_exists(postgres_url, database_name)
    create_database(postgres_url, database_name)
    assert database_exists(postgres_url, database_name)


def test_sqlite_database_does_not_exist(database_name):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, database_name)
        db_url = f'sqlite:///{path}?isolation_level=IMMEDIATE'
        assert not database_exists(db_url, database_name)


def test_sqlite_create_database(database_name):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, database_name)
        db_url = f'sqlite:///{path}?isolation_level=IMMEDIATE'
        assert not database_exists(db_url, database_name)
        create_database(db_url, database_name)
        assert database_exists(db_url, database_name)
