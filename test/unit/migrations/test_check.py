import os
import tempfile

import pytest
from sqlalchemy import (
    create_engine, 
    MetaData, 
    Table,
)
from sqlalchemy_utils import (
    create_database, 
    database_exists,
)
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory

from galaxy.model.migrations.check import (
    DBOutdatedError, 
    NoAlembicVersioningError,
    NoMigrateVersioningError,
    run, 
)
from galaxy.model.migrations.utils import (
    ALEMBIC_TABLE,
    COLUMN_ATTRIBUTES_TO_VERIFY,
    TYPE_ATTRIBUTES_TO_VERIFY,
    MetaDataComparator,
)
from mapping import state0, state2, state3, state5


"""
CASES: 
1. no db >> create, initialize, add alembic
2. empty db >> initialize, add alembic
3. nonempty db, alembic, up-to-date, w/data >> do nothing
4. nonempty db, no alembic, no migrate >> fail, error message: manual upgrade
5. nonempty db, no alembic, migrate >> fail, error message: run migrate+alembic upgrade script
6. nonempty db, alembic >> fail, error message: run alembic upgrade script
"""

#TODO maybe define state imports as fixtures?
#@pytest.fixture
#def state0():
#    return state0
#

@pytest.fixture
def dburl():
    with tempfile.NamedTemporaryFile() as f:
        yield 'sqlite:///%s' % f.name


def test_case_1(dburl):
    """No database."""
    state = state0
    metadata = state.metadata
    assert not database_exists(dburl)

    run(dburl, metadata)
    assert_schema_loaded(dburl, metadata)
    assert_alembic_versioned(dburl)
    

def test_case_2(dburl):
    """Empty database."""
    state = state0
    metadata = state.metadata
    create_database(dburl)

    run(dburl, metadata)
    assert_schema_loaded(dburl, metadata)
    assert_alembic_versioned(dburl)


def test_case_3(dburl):
    """Everything is up-to-date."""
    state = state5
    metadata = state.metadata
    create_database(dburl)
    load_schema(dburl, metadata)
    load_data(dburl, state)
    stamp_alembic(dburl)

    run(dburl, metadata)
    assert_schema_loaded(dburl, metadata)
    assert_alembic_versioned(dburl)
    assert_data(dburl, state)


def test_case_4(dburl):
    """Nonempty database, no alembic, no migrate."""
    state = state0
    metadata = state.metadata
    create_database(dburl)
    load_schema(dburl, metadata)
    load_data(dburl, state)
    with pytest.raises(NoMigrateVersioningError):
        run(dburl, metadata)


def test_case_4_automigrate(dburl):
    """Nonempty database, no alembic, no migrate. Auto-migrate."""
    #TODO


def test_case_5(dburl):
    """Nonempty database, no alembic, migrate."""
    state = state2
    metadata = state.metadata
    create_database(dburl)
    load_schema(dburl, metadata)
    load_data(dburl, state)
    with pytest.raises(NoAlembicVersioningError):
        run(dburl, metadata)


def test_case_5_automigrate(dburl):
    """Nonempty database, no alembic, migrate. Auto-migrate"""
    #TODO


def test_case_6(dburl):
    """Nonempty database, alembic-versioned, out-of-date."""
    state = state3
    metadata = state.metadata
    create_database(dburl)
    load_schema(dburl, metadata)
    load_data(dburl, state)
    stamp_alembic(dburl)

    cfg = Config()
    cfg.set_main_option('script_location', 'lib/galaxy/model/migrations/alembic') #TODO fix path creation!
    cfg.set_main_option('sqlalchemy.url', dburl)
    script = ScriptDirectory.from_config(cfg)
    rev_id, rev_msg = 'new_rev', 'tmp'
    try:
        script.generate_revision(rev_id, rev_msg)
        with pytest.raises(DBOutdatedError):
            run(dburl, metadata)
    finally:
        revision = script.get_revision(rev_id)
        os.remove(revision.path)


def test_case_6_automigrate():
    """Nonempty database, alembic-versioned, out-of-date. Auto-migrate."""
#    create_db()
#    load_schema_and_data(mapping_v3)
#    stamp_alembic()
#
#    cfg = Config("alembic.ini")
#    script = ScriptDirectory.from_config(cfg)
#    rev_id, rev_msg = 'new_rev', 'tmp'
#   # try:
#   #     script.generate_revision(rev_id, rev_msg)
#   #     run(URL, auto_migrate=True)
#   #     # problem: alembic revisions != mapping files in states/
#   #     assert_schema_loaded()
#   #     assert_alembic_versioned()
#   #     assert_data(mapping_v3)
#   # finally:
#   #     revision = script.get_revision(rev_id)
#   #     os.remove(revision.path)





# for test6, use a temp dir
# TODO: maybe use a temp dir for all cases? There's no need to use the real alembic repository?
 
################# test utilities #################

def load_schema(url, metadata):
    with create_engine(url).connect() as conn:
        metadata.bind = conn
        metadata.create_all()
    assert_schema_loaded(url, metadata)


def load_data(url, state):
    with create_engine(url).connect() as conn:
        db_metadata = MetaData(bind=conn)
        db_metadata.reflect()
        for table in db_metadata.sorted_tables:
            ins = table.insert().values(state.data[table.name])
            conn.execute(ins)
    assert_data(url, state)


def stamp_alembic(url):
    cfg = Config()
    cfg.set_main_option('script_location', 'lib/galaxy/model/migrations/alembic') #TODO fix path creation!
    cfg.set_main_option('sqlalchemy.url', url)
    command.stamp(cfg, "head")


def assert_schema_loaded(url, metadata):
    """Assert that db schema is same as schema in metadata."""
    with create_engine(url).connect() as conn:
        db_metadata = MetaData(bind=conn)
        db_metadata.reflect()

    MetaDataComparator().compare(
        db_metadata, metadata, COLUMN_ATTRIBUTES_TO_VERIFY, TYPE_ATTRIBUTES_TO_VERIFY)


def assert_alembic_versioned(url):
    """Assert that db is under alembic version control."""
    with create_engine(url).connect() as conn:
        metadata = MetaData(bind=conn)
        metadata.reflect()
        assert ALEMBIC_TABLE in metadata.tables, 'Database is not under alembic version control'

def assert_data(url, state):
    """Assert that data in db is the same as defined in state.data."""

    def assert_table_data(table_name):
        db_data = conn.execute('select * from %s' % table_name).fetchall()
        # Assert that data in database is the same as the data devined in mapping* module.
        assert db_data == state.data[table_name]

    with create_engine(url).connect() as conn:
        if state in (state0, state5):
            assert_table_data('dataset')
        #if mapping in (mapping_v1, mapping_v2, mapping_v3, mapping_current):
        #    assert_table_data('history')
        #    assert_table_data('hda')
        #if mapping in (mapping_v2, mapping_v3, mapping_current):
        #    assert_table_data('migrate_version')
        #if mapping in (mapping_v3, mapping_current):
        #    assert_table_data('foo2')
        ## we do not test mapping_v4 because that's just for adding alembic
        #if mapping == mapping_current:
        #    assert_table_data('foo3')

