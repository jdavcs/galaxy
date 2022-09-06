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
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
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


GXY_BRANCH_LABEL = 'gxy'
TSI_BRANCH_LABEL = 'tsi'
GXY_BASE_ID = 'gxy0'
TSI_BASE_ID = 'tsi0'


@pytest.fixture()
def tmp_directory():
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture()
def alembic_config_factory(tmp_directory, monkeypatch):

    def f(dburl):
        # initialize alembic directory in testing location
        alembic_dir = os.path.join(tmp_directory, 'alembic')
        alembic_config = Config(os.path.join(alembic_dir, "alembic.ini"))
        alembic.command.init(alembic_config, alembic_dir)  # TODO errors on mult tests
        alembic_config.set_main_option("sqlalchemy.url", dburl)
        # Create gxy and tsi branches (MUST SET head='base'!)
        alembic.command.revision(alembic_config, branch_label=GXY_BRANCH_LABEL, head='base', rev_id=GXY_BASE_ID)
        alembic.command.revision(alembic_config, branch_label=TSI_BRANCH_LABEL, head='base', rev_id=TSI_BASE_ID)
        # Use the test alembic.ini file
        monkeypatch.setenv('ALEMBIC_CONFIG', alembic_config.config_file_name)
        # Use the test dburl
        monkeypatch.setenv('GALAXY_CONFIG_OVERRIDE_DATABASE_CONNECTION', dburl)
        monkeypatch.setenv('GALAXY_CONFIG_OVERRIDE_INSTALL_DATABASE_CONNECTION', dburl)
        return alembic_config

    return f


def stdout(capture):
    return capture.readouterr().out


def run_command(cmd):
    #completed_process = subprocess.run(cmd.split())  # for debugging only
    completed_process = subprocess.run(cmd.split(), capture_output=True, text=True)  # TODO uncomment when done
    return completed_process


class TestRevisionCommand:

    def test_revision_cmd(self, url_factory, alembic_config_factory, monkeypatch):
        # setup
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)

        # run command under test
        run_command(f"./db.sh revision --message foo1")  # rev-id is optional
        run_command(f"./db.sh revision --rev-id 2 --message foo2")
        run_command(f"./db.sh revision --rev-id 3 --message foo3")

        # get result and assert
        script_dir = ScriptDirectory.from_config(alembic_cfg)
        revisions = [rev for rev in script_dir.walk_revisions()]
        assert len(revisions) == 5  # 2 base + 3 new

        rev = script_dir.get_revision('3')
        assert rev.revision == '3'  # verify revision id
        assert GXY_BRANCH_LABEL in rev.branch_labels  # verify branch label
        assert rev.down_revision == '2'  # verify parent revision
        assert rev.module.__name__ == '3_foo3_py'  # verify message

    def test_revision_cmd_missing_message_arg_error(self, url_factory, alembic_config_factory, monkeypatch):
        # setup
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)

        # run command under test
        completed = run_command(f"./db.sh revision --rev-id 1")

        assert completed.returncode == 2
        assert "the following arguments are required: -m/--message" in completed.stderr


class TestShowCommand:

    def test_show_cmd(self, url_factory, alembic_config_factory, monkeypatch):
        # setup
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)

        alembic.command.revision(alembic_cfg, rev_id='42', head=GXY_BASE_ID)

        # run command under test
        completed = run_command(f"./db.sh show 42")

        assert "Revision ID: 42" in completed.stdout

    def test_show_cmd_invalid_revision_error(self, url_factory, alembic_config_factory, monkeypatch):
        # setup
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)

        alembic.command.revision(alembic_cfg, rev_id='42', head=GXY_BASE_ID)

        completed = run_command(f"./db.sh show idonotexist")
        assert completed.returncode == 1
        assert "Can't locate revision identified by 'idonotexist'" in completed.stderr

    def test_show_cmd_missing_revision_arg_error(self, url_factory, alembic_config_factory, monkeypatch):
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)

        completed = run_command(f"./db.sh show")
        assert completed.returncode == 2
        assert "the following arguments are required: revision" in completed.stderr


class TestHistoryCommand:

    def test_history_cmd(self, url_factory, alembic_config_factory, monkeypatch):
        # setup
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)

        alembic.command.revision(alembic_cfg, rev_id='1', head=GXY_BASE_ID)
        alembic.command.revision(alembic_cfg, rev_id='2', head='1')
        alembic.command.revision(alembic_cfg, rev_id='3', head='2')

        # run command under test
        completed = run_command(f"./db.sh history")

        assert completed.returncode == 0
        assert "2 -> 3 (gxy) (head), empty message" in completed.stdout
        assert "1 -> 2 (gxy)" in completed.stdout
        assert "gxy0 -> 1 (gxy)" in completed.stdout

    def test_history_cmd_verbose(self, url_factory, alembic_config_factory, monkeypatch):
        # setup
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)

        alembic.command.revision(alembic_cfg, rev_id='1', head=GXY_BASE_ID)
        alembic.command.revision(alembic_cfg, rev_id='2', head='1')
        alembic.command.revision(alembic_cfg, rev_id='3', head='2')

        # run command under test
        completed = run_command(f"./db.sh history --verbose")

        assert "Revision ID: 2" in completed.stdout
        assert "Revises: 1" in completed.stdout

    def test_history_cmd_indicate_current(self, url_factory, alembic_config_factory, monkeypatch):
        # setup
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)

        alembic.command.revision(alembic_cfg, rev_id='1', head=GXY_BASE_ID)
        alembic.command.revision(alembic_cfg, rev_id='2', head='1')
        alembic.command.revision(alembic_cfg, rev_id='3', head='2')

        # required for indicating current version
        alembic.command.upgrade(alembic_cfg, 'heads')

        completed = run_command(f"./db.sh history --indicate-current")

        assert completed.returncode == 0
        assert "2 -> 3 (gxy) (head) (current), empty message" in completed.stdout
        assert "1 -> 2 (gxy)" in completed.stdout
        assert "gxy0 -> 1 (gxy)" in completed.stdout


class TestVersionCommand:

    def test_version_cmd(self, url_factory, alembic_config_factory, monkeypatch):
        # setup
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)

        alembic.command.revision(alembic_cfg, rev_id='1', head=GXY_BASE_ID)
        alembic.command.revision(alembic_cfg, rev_id='2', head='1')

        # run command under test
        completed = run_command(f"./db.sh version")

        assert completed.returncode == 0
        assert "2 (gxy) (head)" in completed.stdout

    def test_version_cmd_verbose(self, url_factory, alembic_config_factory, monkeypatch):
        # setup
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)

        alembic.command.revision(alembic_cfg, rev_id='1', head=GXY_BASE_ID)
        alembic.command.revision(alembic_cfg, rev_id='2', head='1')

        # run command under test
        completed = run_command(f"./db.sh version --verbose")

        assert completed.returncode == 0
        assert "Revision ID: 2" in completed.stdout
        assert "Revises: 1" in completed.stdout


class TestUpgradeCommand:

    def test_upgrade_cmd(self, url_factory, alembic_config_factory, monkeypatch):
        # setup
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)

        alembic.command.revision(alembic_cfg, rev_id='1', head=GXY_BASE_ID)
        alembic.command.revision(alembic_cfg, rev_id='2', head='1')

        completed = run_command(f"./db.sh upgrade")  # upgrade gxy to v2, tsi to base
        assert completed.returncode == 0
        assert "Running upgrade gxy0 -> 1" in completed.stderr
        assert "Running upgrade 1 -> 2" in completed.stderr

        engine = create_engine(dburl)
        with engine.connect() as conn:
            context = MigrationContext.configure(conn)
            heads = context.get_current_heads()
            assert len(heads) == 2
            assert '2' in heads
            assert '3' not in heads

        alembic.command.revision(alembic_cfg, rev_id='3', head='2')

        completed = run_command(f"./db.sh upgrade")  # upgrade gxy to v3
        assert completed.returncode == 0
        assert "Running upgrade 2 -> 3" in completed.stderr

        with engine.connect() as conn:
            context = MigrationContext.configure(conn)
            heads = context.get_current_heads()
            assert len(heads) == 2
            assert '2' not in heads
            assert '3' in heads

        engine.dispose()

    def test_upgrade_cmd_sql_only(self, url_factory, alembic_config_factory, monkeypatch):
        # setup
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)

        alembic.command.revision(alembic_cfg, rev_id='1', head=GXY_BASE_ID)
        alembic.command.revision(alembic_cfg, rev_id='2', head='1')

        completed = run_command(f"./db.sh upgrade --sql")  # upgrade gxy to v2, tsi to base
        assert completed.returncode == 0
        assert "UPDATE alembic_version SET version_num='2'" in completed.stdout
        assert "UPDATE alembic_version SET version_num='3'" not in completed.stdout

        alembic.command.revision(alembic_cfg, rev_id='3', head='2')

        completed = run_command(f"./db.sh upgrade --sql")  # upgrade gxy to v3
        assert completed.returncode == 0
        assert "UPDATE alembic_version SET version_num='2'" in completed.stdout
        assert "UPDATE alembic_version SET version_num='3'" in completed.stdout

    def test_upgrade_cmd_with_revision_arg(self, url_factory, alembic_config_factory, monkeypatch):
        # setup
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)
        # TODO
        # implement +1 as gxy@+1; test also for rev+1, and same for downgrading.


class TestDowngradeCommand:

    def test_downgrade_cmd(self, url_factory, alembic_config_factory, monkeypatch):
        # setup
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)

        alembic.command.revision(alembic_cfg, rev_id='1', head=GXY_BASE_ID)
        alembic.command.revision(alembic_cfg, rev_id='2', head='1')
        alembic.command.revision(alembic_cfg, rev_id='3', head='2')
        alembic.command.upgrade(alembic_cfg, 'heads')

        completed = run_command(f"./db.sh downgrade 1")  # upgrade gxy to v2, tsi to base
        assert completed.returncode == 0
        assert "Running downgrade 3 -> 2" in completed.stderr
        assert "Running downgrade 2 -> 1" in completed.stderr

        engine = create_engine(dburl)
        with engine.connect() as conn:
            context = MigrationContext.configure(conn)
            heads = context.get_current_heads()
            assert len(heads) == 2
            assert '1' in heads

        engine.dispose()


class TestDbVersionCommand:

    def test_dbversion_cmd(self, url_factory, alembic_config_factory, monkeypatch):
        # setup
        dburl = url_factory()
        alembic_cfg = alembic_config_factory(dburl)

        alembic.command.revision(alembic_cfg, rev_id='1', head=GXY_BASE_ID)
        alembic.command.revision(alembic_cfg, rev_id='2', head='1')

        completed = run_command(f"./db.sh dbversion")  # upgrade gxy to v2, tsi to base
        assert completed.returncode == 0
        assert "(head)" not in completed.stdout  # there has been no upgrade

        alembic.command.upgrade(alembic_cfg, 'heads')

        completed = run_command(f"./db.sh dbversion")  # upgrade gxy to v2, tsi to base
        assert completed.returncode == 0
        assert "2 (head)" in completed.stdout



# TODO: upgrade + downgrade with different rev arguments, dbversion, 
#    def assert_alembic_revision_command_output(self, output, rev_id):
#        pattern = re.compile(rf"\s*Generating /.+/alembic/versions/{rev_id}_.py ...  done")
#        assert pattern.match(output)
#
#
#
