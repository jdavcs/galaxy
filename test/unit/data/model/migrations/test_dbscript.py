import os
import re
import tempfile
import subprocess
import uuid
from contextlib import contextmanager
from typing import (
    Callable,
    Iterator,
    NewType,
    Optional,
)


import alembic
from alembic.config import Config
from alembic import command

from sqlalchemy import (
    create_engine,
    delete,
    select,
)
from sqlalchemy.engine import (
    Engine,
    make_url,
)
from sqlalchemy.sql.compiler import IdentifierPreparer

from galaxy.model.database_utils import create_database
import pytest

from galaxy.model.database_utils import database_exists
from galaxy.model.migrations.scripts import DbScript
from ..testing_utils import (  # noqa: F401  (url_factory is a fixture we have to import explicitly)
    create_and_drop_database,
    disposing_engine,
    drop_existing_database,
    url_factory,
)

DbUrl = NewType("DbUrl", str)


@pytest.fixture(scope="module")
def tmp_directory2():
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir

@pytest.fixture
def url_factory2(tmp_directory2) -> Callable[[], DbUrl]:

    def url(envvar=None) -> DbUrl:
        envvar = envvar or "GALAXY_TEST_DBURI"
        database = _generate_unique_database_name2()
        connection_url = _get_connection_url2(envvar)
        if connection_url:
            return _make_postgres_db_url(DbUrl(connection_url), database)
        else:
            return _make_sqlite_db_url(tmp_directory2, database)

    return url

def _generate_unique_database_name2() -> str:
    return f"galaxytest_{uuid.uuid4().hex}"

def _get_connection_url2(envvar):
    return os.environ.get(envvar)

def _make_sqlite_db_url(tmpdir: str, database: str) -> DbUrl:
    path = os.path.join(tmpdir, database)
    return DbUrl(f"sqlite:///{path}")


def _make_postgres_db_url(connection_url: DbUrl, database: str) -> DbUrl:
    url = make_url(connection_url)
    url = url.set(database=database)
    return DbUrl(str(url))



@pytest.fixture()
def alembic_config_factory(tmp_directory):

    def f(dburl):
        alembic_dir = os.path.join(tmp_directory, 'alembic')
        alembic_config = Config(os.path.join(alembic_dir, "alembic.ini"))
        alembic.command.init(alembic_config, alembic_dir)
        alembic_config.set_main_option("sqlalchemy.url", dburl)
        alembic_config.set_main_option("script_location", alembic_dir)
        return alembic_config

    return f


def stdout(capture):
    return capture.readouterr().out



class TestDbScript:

    def test_revision(self, url_factory, alembic_config_factory, monkeypatch):
        dburl = url_factory()  # construct a db url
        create_database(dburl)  # maybe use a context manager?
        alembic_cfg = alembic_config_factory(dburl)  # make alembic.Config object

        monkeypatch.setenv('ALEMBIC_CONFIG', alembic_cfg.config_file_name)  # set envvar for this test to point to the alembic config object

        #self.run_command(f"./db.sh revision --rev-id 1 --message foo")
        self.run_command(f"./db.sh revision  --message foo")
        self.run_command(f"./db.sh revision  --message foo")
        #self.verify_head_revision(id="2", message="bar")

        #self.run_command(f"./db.sh revision --rev-id 2 --message bar")
        #self.verify_head_revision(id="2", message="bar")


        #completed = self.run_command(f"./db.sh revision --message foo444")
        #completed = self.run_command(f"./db.sh history")



        #self.run_command(f"./db.sh revision --rev-id 2 --message bar")
        #self.verify_head_revision(id="2", message="bar")

    def run_command(self, cmd):
        completed_process = subprocess.run(cmd.split())  # for debugging only
        #completed_process = subprocess.run(cmd.split(), capture_output=True)  # TODO uncomment when done
        assert completed_process.returncode == 0
        return completed_process


    def get_head_revision(self, alembic_cfg):
        #revision = alembic_cfg.
        pass

    def verify_head_revision(self, id, message):
        pass
    #head = self.get_head_revision(alembic_cfg)
    #    assert head.id == id
    #    assert head.message == message

    def __test_verify_alembic(self, url_factory, alembic_config_factory, capsys):
        dburl = url_factory()
        create_database(dburl)  # maybe use context manager
        alembic_cfg = alembic_config_factory(dburl)
        capsys.readouterr()

        # Create revision 1
        alembic.command.revision(alembic_cfg, rev_id='1')
        foo1 = capsys.readouterr().out
        #self.assert_alembic_revision_command_output(stdout(capsys), rev_id='1')

        # Create revision 2
        alembic.command.revision(alembic_cfg, rev_id='2')
        #self.assert_alembic_revision_command_output(stdout(capsys), rev_id='2')
        foo2 = capsys.readouterr().out

        # Current version not set
        #alembic.command.current(alembic_cfg)
        #assert stdout(capsys) == ''

        alembic.command.heads(alembic_cfg)  # why no stdout???????
        #alembic.command.revision(alembic_cfg)
        foo3 = capsys.readouterr().out
        #foo = capsys.readouterr()
        #assert stdout(capsys) == ''

        alembic.command.revision(alembic_cfg)
        foo4 = capsys.readouterr().out
        #breakpoint()

        #foo = stdout(capsys)
        #breakpoint()

        # assert stdout == pattern

        #alembic.command.revision(alembic_cfg, rev_id='2')
        #alembic.command.revision(alembic_cfg, rev_id='3')
        #alembic.command.history(alembic_cfg)

        #alembic.command.heads(alembic_cfg)
        ## assert smth

        #alembic.command.current(alembic_cfg)
        ## assert smth

        #command.upgrade(alembic_cfg, "heads")
        # assert smth

    def assert_alembic_revision_command_output(self, output, rev_id):
        pattern = re.compile(rf"\s*Generating /.+/alembic/versions/{rev_id}_.py ...  done")
        assert pattern.match(output)





    def backup_test_draft_verify_alembic(self, url_factory2, tmp_directory2):
        """ Verify Alembic setup: should be functional and operate as expected.
        """
        # create db
        # connect to db
        # init db to some state
        # call the script
        # verify script output
        # optional: verify version in db or directory

        dburl = url_factory2('MYDB1') 
        create_database(dburl)

        alembic_dir = os.path.join(tmp_directory2, 'alembic')
        alembic_cfg = Config(os.path.join(alembic_dir, "alembic.ini"))
        alembic.command.init(alembic_cfg, alembic_dir)
        alembic_cfg.set_main_option("sqlalchemy.url", dburl)



# the test 
        alembic.command.revision(alembic_cfg, rev_id='1')
        alembic.command.revision(alembic_cfg, rev_id='2')
        alembic.command.revision(alembic_cfg, rev_id='3')
        alembic.command.history(alembic_cfg)

        alembic.command.heads(alembic_cfg)
        # assert smth

        alembic.command.current(alembic_cfg)
        # assert smth

        command.upgrade(alembic_cfg, "heads")
        # assert smth



        #engine = create_engine(dburl)
        #with engine.begin() as connection:
        #    alembic.command.history(alembic_cfg)
        #    alembic.command.revision(alembic_cfg)
        #    alembic.command.revision(alembic_cfg)
        #    alembic.command.revision(alembic_cfg)
        #    alembic.command.history(alembic_cfg)
        #    alembic.command.heads(alembic_cfg)
        #    alembic.command.current(alembic_cfg)

        #    command.upgrade(alembic_cfg, "heads")


        #    #alembic_cfg.attributes['connection'] = connection  # this doesn't work. because env.py doesn't use it!
        #    #alembic.command.upgrade(alembic_cfg, 'head')

        #engine.dispose()


# maybe run alembic programmatically?
        #subprocess.run(['alembic', 'history'])


        #engine = create_engine(dburl)
        #assert database_exists(dburl)

        #env.invoke('db.sh', 'version')

        #tmp_directory = tmp_directory2



    #with tempfile.TemporaryDirectory() as tmp_dir:
    #    yield tmp_dir

#        db_url = url_factory()
#
#        monkeypatch.setenv('FOO', 'postgresql://galaxy:42@localhost:5432/galaxy22222')
#
#        with create_and_drop_database(db_url):
#            with disposing_engine(db_url) as engine:
#                assert database_exists(db_url)
#
#                subprocess.run(['./db.sh', 'version'])
#
#                # call command
#
##                assert database_is_up_to_date(db_url, metadata_state6_combined, GXY)
##                assert database_is_up_to_date(db_url, metadata_state6_combined, TSI)
#
#        # maybe assert stdout?
#
#        # maybe test exit code and output?
#        #env = TestEnv()
#        #env.db = make_db(state1)
#        #env.dir = tempdir.mkdir()
#        #env.invoke('db.sh', 'version')
#        # assert that db is upgraded?


        pass
         

        
def database_is_up_to_date(db_url, current_state_metadata, model):
    # True if the database at `db_url` has the `current_state_metadata` loaded,
    # and is up-to-date with respect to `model` (has the most recent Alembic revision).

    # NOTE: Ideally, we'd determine the current metadata based on the model. However, since
    # metadata is a fixture, it cannot be called directly, and instead has to be
    # passed as an argument. That's why we ensure that the passed metadata is current
    # (this guards againt an incorrect test).
    if model == GXY:
        current_tables = {"gxy_table1", "gxy_table2", "gxy_table3"}
    elif model == TSI:
        current_tables = {"tsi_table1", "tsi_table2", "tsi_table3"}
    is_metadata_current = current_tables <= set(current_state_metadata.tables)

    with disposing_engine(db_url) as engine:
        is_loaded = is_metadata_loaded(db_url, current_state_metadata)
        am = AlembicManagerForTests(engine)
        return is_metadata_current and is_loaded and am.is_up_to_date(model)

