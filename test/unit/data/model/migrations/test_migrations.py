import os
from typing import Union

import pytest
from sqlalchemy import MetaData

from galaxy.model import migrations
from galaxy.model.database_utils import database_exists
from galaxy.model.migrations import (
    AlembicManager,
    DatabaseStateCache,
    DatabaseVerifier,
    GXY,
    listify,
    load_metadata,
    NoVersionTableError,
    OutdatedDatabaseError,
    SQLALCHEMYMIGRATE_LAST_VERSION,
    SQLALCHEMYMIGRATE_TABLE,
    TSI,
    VersionTooOldError,
)
from .common import (
    create_and_drop_database,
    disposing_engine,
)

# Revision numbers from test versions directories
GXY_REVISION_0 = '62695fac6cc0'  # oldest/base
GXY_REVISION_1 = '2e8a580bc79a'
GXY_REVISION_2 = 'e02cef55763c'  # current/head
TSI_REVISION_0 = '1bceec30363a'  # oldest/base
TSI_REVISION_1 = '8364ef1cab05'
TSI_REVISION_2 = '0e28bf2fb7b5'  # current/head


def test_foo(url_factory):
    db_url = url_factory()
    assert not database_exists(db_url)
    with create_and_drop_database(db_url):
        assert database_exists(db_url)


#class TestAlembicManager:
#
#    def test_is_at_revision__one_head_one_revision(self, url_factory):
#        """ Use case: Check if separate tsi database is at a given revision."""
#        db_url = url_factory()
#        with create_and_drop_database(db_url):
#            with disposing_engine(db_url) as engine:
#                am = AlembicManagerForTests(engine)
#                revision = GXY_REVISION_0
#                assert not am.is_at_revision(revision)
#                am.stamp(revision)
#                assert am.is_at_revision(revision)
#
#    def test_is_at_revision__two_heads_one_revision(self, url_factory):
#        """ Use case: Check if combined gxy and tsi database is at a given gxy revision."""
#        db_url = url_factory()
#        with create_and_drop_database(db_url):
#            with disposing_engine(db_url) as engine:
#                am = AlembicManagerForTests(engine)
#                revision = GXY_REVISION_0
#                revisions = [GXY_REVISION_0, TSI_REVISION_0]
#                assert not am.is_at_revision(revision)
#                am.stamp(revisions)
#                assert am.is_at_revision(revision)
#
#    def test_is_at_revision__two_heads_two_revisions(self, url_factory):
#        """ Use case: Check if combined gxy and tsi database is at given gxy and tsi revisions."""
#        db_url = url_factory()
#        with create_and_drop_database(db_url):
#            with disposing_engine(db_url) as engine:
#                am = AlembicManagerForTests(engine)
#                revisions = [GXY_REVISION_0, TSI_REVISION_0]
#                assert not am.is_at_revision(revisions)
#                am.stamp(revisions)
#                assert am.is_at_revision(revisions)
#
#    def test_is_up_to_date_single_revision(self, url_factory):
#        db_url = url_factory()
#        with create_and_drop_database(db_url):
#            with disposing_engine(db_url) as engine:
#                model = GXY
#                am = AlembicManagerForTests(engine)
#                assert not am.is_up_to_date(model)
#                am.stamp(GXY_REVISION_1)
#                assert not am.is_up_to_date(model)
#                am.stamp(GXY_REVISION_2)
#                assert am.is_up_to_date(model)
#
#    def test_not_is_up_to_date_wrong_model(self, url_factory):
#        db_url = url_factory()
#        with create_and_drop_database(db_url):
#            with disposing_engine(db_url) as engine:
#                am = AlembicManagerForTests(engine)
#                assert not am.is_up_to_date(GXY)
#                assert not am.is_up_to_date(TSI)
#                am.stamp(GXY_REVISION_2)
#                assert am.is_up_to_date(GXY)
#                assert not am.is_up_to_date(TSI)
#
#    def test_is_up_to_date_multiple_revisions(self, url_factory):
#        db_url = url_factory()
#        with create_and_drop_database(db_url):
#            with disposing_engine(db_url) as engine:
#                am = AlembicManagerForTests(engine)
#                assert not am.is_up_to_date(GXY)  # False: no head revisions in database
#                am.stamp([GXY_REVISION_2, TSI_REVISION_2])
#                assert am.is_up_to_date(GXY)  # True: both are up-to-date
#                assert am.is_up_to_date(TSI)  # True: both are up-to-date
#
#    def test_is_not_up_to_date_multiple_revisions_both(self, url_factory):
#        db_url = url_factory()
#        with create_and_drop_database(db_url):
#            with disposing_engine(db_url) as engine:
#                am = AlembicManagerForTests(engine)
#                am.stamp([GXY_REVISION_1, TSI_REVISION_1])
#                assert not am.is_up_to_date(GXY)  # False: both are not up-to-date
#                assert not am.is_up_to_date(TSI)  # False: both are not up-to-date
#
#    def test_is_not_up_to_date_multiple_revisions_one(self, url_factory):
#        db_url = url_factory()
#        with create_and_drop_database(db_url):
#            with disposing_engine(db_url) as engine:
#                am = AlembicManagerForTests(engine)
#                am.stamp([GXY_REVISION_2, TSI_REVISION_1])
#                assert am.is_up_to_date(GXY)  # True
#                assert not am.is_up_to_date(TSI)  # False: only one is up-to-date
#
#


    #class TestDatabaseStateCache:
    #
    #    def test_is_empty(self, url_factory, metadata_state1_gxy):
    #        db_url, metadata = url_factory(), metadata_state1_gxy
    #        with create_and_drop_database(db_url):
    #            with disposing_engine(db_url) as engine:
    #                assert DatabaseStateCache(engine).is_database_empty()
    #                with engine.connect() as conn:
    #                    metadata.create_all(bind=conn)
    #                assert not DatabaseStateCache(engine).is_database_empty()
    #
#    def test_has_alembic_version_table(self, url_factory, metadata_state4_gxy):
#        db_url, metadata = url_factory(), metadata_state4_gxy
#        with create_and_drop_database(db_url):
#            with disposing_engine(db_url) as engine:
#                assert not DatabaseStateCache(engine).has_alembic_version_table()
#                with engine.connect() as conn:
#                    metadata.create_all(bind=conn)
#                assert DatabaseStateCache(engine).has_alembic_version_table()
#
#    def test_has_sqlalchemymigrate_version_table(self, url_factory, metadata_state2_gxy):
#        db_url, metadata = url_factory(), metadata_state2_gxy
#        with create_and_drop_database(db_url):
#            with disposing_engine(db_url) as engine:
#                assert not DatabaseStateCache(engine).has_sqlalchemymigrate_version_table()
#                with engine.connect() as conn:
#                    metadata.create_all(bind=conn)
#                assert DatabaseStateCache(engine).has_sqlalchemymigrate_version_table()
#
#    def test_is_last_sqlalchemymigrate_version(self, url_factory, metadata_state2_gxy):
#        db_url = url_factory()
#        with create_and_drop_database(db_url):
#            with disposing_engine(db_url) as engine:
#                load_metadata(metadata_state2_gxy, engine)
#                load_sqlalchemymigrate_version(db_url, SQLALCHEMYMIGRATE_LAST_VERSION - 1)
#                assert not DatabaseStateCache(engine).is_last_sqlalchemymigrate_version()
#                load_sqlalchemymigrate_version(db_url, SQLALCHEMYMIGRATE_LAST_VERSION)
#                assert DatabaseStateCache(engine).is_last_sqlalchemymigrate_version()


## Database fixture tests
#
#class TestDatabaseFixtures:
#    """
#    Verify that database fixtures have the expected state.
#
#    The fixtures of the form `db_state#_[gxy|tsi]` are urls that point
#    to databases that HAVE BEEN CREATED. Thus, we are not wrapping them here
#    in the `create_and_drop_database` context manager: they are wrapped already.
#    """
#    class TestState1:
#
#        def test_database_gxy(self, db_state1_gxy, metadata_state1_gxy):
#            self.verify_state(db_state1_gxy, metadata_state1_gxy)
#
#        def test_database_tsi(self, db_state1_tsi, metadata_state1_tsi):
#            self.verify_state(db_state1_tsi, metadata_state1_tsi)
#
#        def test_database_combined(self, db_state1_combined, metadata_state1_combined):
#            self.verify_state(db_state1_combined, metadata_state1_combined)
#
#        def verify_state(self, db_url, metadata):
#            assert is_metadata_loaded(db_url, metadata)
#            with disposing_engine(db_url) as engine:
#                db = DatabaseStateCache(engine)
#                assert not db.has_sqlalchemymigrate_version_table()
#                assert not db.has_alembic_version_table()
#
#    class TestState2:
#
#        def test_database_gxy(self, db_state2_gxy, metadata_state2_gxy):
#            self.verify_state(db_state2_gxy, metadata_state2_gxy)
#
#        def test_database_tsi(self, db_state2_tsi, metadata_state2_tsi):
#            self.verify_state(db_state2_tsi, metadata_state2_tsi)
#
#        def test_database_combined(self, db_state2_combined, metadata_state2_combined):
#            self.verify_state(db_state2_combined, metadata_state2_combined)
#
#        def verify_state(self, db_url, metadata):
#            assert is_metadata_loaded(db_url, metadata)
#            with disposing_engine(db_url) as engine:
#                db = DatabaseStateCache(engine)
#                assert db.has_sqlalchemymigrate_version_table()
#                assert not db.is_last_sqlalchemymigrate_version()
#                assert not db.has_alembic_version_table()
#
#    class TestState3:
#
#        def test_database_gxy(self, db_state3_gxy, metadata_state3_gxy):
#            self.verify_state(db_state3_gxy, metadata_state3_gxy)
#
#        def test_database_tsi(self, db_state3_tsi, metadata_state3_tsi):
#            self.verify_state(db_state3_tsi, metadata_state3_tsi)
#
#        def test_database_combined(self, db_state3_combined, metadata_state3_combined):
#            self.verify_state(db_state3_combined, metadata_state3_combined)
#
#        def verify_state(self, db_url, metadata):
#            assert is_metadata_loaded(db_url, metadata)
#            with disposing_engine(db_url) as engine:
#                db = DatabaseStateCache(engine)
#                assert db.has_sqlalchemymigrate_version_table()
#                assert db.is_last_sqlalchemymigrate_version()
#                assert not db.has_alembic_version_table()
#
#    class TestState4:
#
#        def test_database_gxy(self, db_state4_gxy, metadata_state4_gxy):
#            self.verify_state(db_state4_gxy, metadata_state4_gxy, GXY_REVISION_0)
#
#        def test_database_tsi(self, db_state4_tsi, metadata_state4_tsi):
#            self.verify_state(db_state4_tsi, metadata_state4_tsi, TSI_REVISION_0)
#
#        def test_database_combined(self, db_state4_combined, metadata_state4_combined):
#            self.verify_state(
#                db_state4_combined, metadata_state4_combined, [GXY_REVISION_0, TSI_REVISION_0])
#
#        def verify_state(self, db_url, metadata, revision):
#            assert is_metadata_loaded(db_url, metadata)
#            with disposing_engine(db_url) as engine:
#                db = DatabaseStateCache(engine)
#                assert db.has_sqlalchemymigrate_version_table()
#                assert db.is_last_sqlalchemymigrate_version()
#                assert db.has_alembic_version_table()
#                assert AlembicManagerForTests(engine).is_at_revision(revision)
#
#    class TestState5:
#
#        def test_database_gxy(self, db_state5_gxy, metadata_state5_gxy):
#            self.verify_state(db_state5_gxy, metadata_state5_gxy, GXY_REVISION_1)
#
#        def test_database_tsi(self, db_state5_tsi, metadata_state5_tsi):
#            self.verify_state(db_state5_tsi, metadata_state5_tsi, TSI_REVISION_1)
#
#        def test_database_combined(self, db_state5_combined, metadata_state5_combined):
#            self.verify_state(
#                db_state5_combined, metadata_state5_combined, [GXY_REVISION_1, TSI_REVISION_1])
#
#        def verify_state(self, db_url, metadata, revision):
#            assert is_metadata_loaded(db_url, metadata)
#            with disposing_engine(db_url) as engine:
#                db = DatabaseStateCache(engine)
#                assert not db.has_sqlalchemymigrate_version_table()
#                assert db.has_alembic_version_table()
#                assert AlembicManagerForTests(engine).is_at_revision(revision)
#
#    class TestState6:
#
#        def test_database_gxy(self, db_state6_gxy, metadata_state6_gxy):
#            self.verify_state(db_state6_gxy, metadata_state6_gxy, GXY_REVISION_2)
#
#        def test_database_tsi(self, db_state6_tsi, metadata_state6_tsi):
#            self.verify_state(db_state6_tsi, metadata_state6_tsi, TSI_REVISION_2)
#
#        def test_database_combined(self, db_state6_combined, metadata_state6_combined):
#            self.verify_state(
#                db_state6_combined, metadata_state6_combined, [GXY_REVISION_2, TSI_REVISION_2])
#
#        def verify_state(self, db_url, metadata, revision):
#            assert is_metadata_loaded(db_url, metadata)
#            with disposing_engine(db_url) as engine:
#                db = DatabaseStateCache(engine)
#                assert not db.has_sqlalchemymigrate_version_table()
#                assert db.has_alembic_version_table()
#                assert AlembicManagerForTests(engine).is_at_revision(revision)
#
#
## Tests of primary function under different scenarios and database state
#
#class TestNoDatabaseState:
#    """
#    Initial state: database does not exist.
#    Expect: database created, initialized, versioned w/alembic.
#    (we use `metadata_state6_{gxy|tsi|combined}` for final database schema)
#    """
#    def test_combined_database(self, url_factory, metadata_state6_combined):
#        db_url = url_factory()
#        assert not database_exists(db_url)
#        with disposing_engine(db_url) as engine:
#            db = DatabaseVerifier(engine)
#            db.verify()
#            assert database_is_up_to_date(db_url, metadata_state6_combined)
#
#    def test_separate_databases(self, url_factory, metadata_state6_gxy, metadata_state6_tsi):
#        db1_url, db2_url = url_factory(), url_factory()
#        assert not database_exists(db1_url)
#        assert not database_exists(db2_url)
#        with disposing_engine(db1_url) as engine1, disposing_engine(db2_url) as engine2:
#            db = DatabaseVerifier(engine1, engine2)
#            db.verify()
#            assert database_is_up_to_date(db1_url, metadata_state6_gxy, GXY)
#            assert database_is_up_to_date(db2_url, metadata_state6_tsi, TSI)
#
#
#class TestDatabaseState0:  # TODO: this exposes the bug in DatabaseVerifier
#    """
#    Initial state: database is empty.
#    Expect: database created, initialized, versioned w/alembic.
#    """
#    def test_combined_database(self, url_factory, metadata_state6_combined):
#        db_url = url_factory()
#        with create_and_drop_database(db_url):
#            with disposing_engine(db_url) as engine:
#                db = DatabaseVerifier(engine)
#                assert database_exists(db_url)
#                assert db._is_database_empty(GXY)
#                db.verify()
#                assert database_is_up_to_date(db_url, metadata_state6_combined)
#
#    def test_separate_databases(self, url_factory, metadata_state6_gxy, metadata_state6_tsi):
#        db1_url, db2_url = url_factory(), url_factory()
#        with create_and_drop_database(db1_url), create_and_drop_database(db2_url):
#            with disposing_engine(db1_url) as engine1, disposing_engine(db2_url) as engine2:
#                db = DatabaseVerifier(engine1, engine2)
#                assert database_exists(db1_url)
#                assert database_exists(db2_url)
#                assert db._is_database_empty(GXY)
#                assert db._is_database_empty(TSI)
#                db.verify()
#                assert database_is_up_to_date(db1_url, metadata_state6_gxy, GXY)
#                assert database_is_up_to_date(db2_url, metadata_state6_tsi, TSI)
#
#
#class TestDatabaseState1:
#    """
#    Initial state: non-empty database, no version table.
#    Expect: fail with appropriate message.
#    """
#    def test_combined_database(self, db_state1_combined):
#        with pytest.raises(NoVersionTableError):
#            with disposing_engine(db_state1_combined) as engine:
#                db = DatabaseVerifier(engine)
#                db.verify()
#
#    def test_separate_databases_gxy_raises_error(self, db_state1_gxy, db_state6_tsi):
#        with pytest.raises(NoVersionTableError):
#            with disposing_engine(db_state1_gxy) as engine1, disposing_engine(db_state6_tsi) as engine2:
#                db = DatabaseVerifier(engine1, engine2)
#                db.verify()
#
#    def test_separate_databases_tsi_raises_error(self, db_state6_gxy, db_state1_tsi):
#        with pytest.raises(NoVersionTableError):
#            with disposing_engine(db_state6_gxy) as engine1, disposing_engine(db_state1_tsi) as engine2:
#                db = DatabaseVerifier(engine1, engine2)
#                db.verify()
#
#
#class TestDatabaseState2:
#    """
#    Initial state: non-empty database, SQLAlchemy Migrate version table present; however,
#    the stored version is not the latest after which we could transition to Alembic.
#    Expect: fail with appropriate message.
#    """
#    def test_combined_database(self, db_state2_combined):
#        with pytest.raises(VersionTooOldError):
#            with disposing_engine(db_state2_combined) as engine:
#                db = DatabaseVerifier(engine)
#                db.verify()
#
#    def test_separate_databases_gxy_raises_error(self, db_state2_gxy, db_state6_tsi):
#        with pytest.raises(VersionTooOldError):
#            with disposing_engine(db_state2_gxy) as engine1, disposing_engine(db_state6_tsi) as engine2:
#                db = DatabaseVerifier(engine1, engine2)
#                db.verify()
#
#    def test_separate_databases_tsi_raises_error(self, db_state6_gxy, db_state2_tsi):
#        with pytest.raises(VersionTooOldError):
#            with disposing_engine(db_state6_gxy) as engine1, disposing_engine(db_state2_tsi) as engine2:
#                db = DatabaseVerifier(engine1, engine2)
#                db.verify()
#
#
#class TestDatabaseState3:
#    """
#    Initial state: non-empty database, SQLAlchemy Migrate version table contains latest version
#    under SQLAlchemy Migrate.
#    Expect:
#    a) auto-migrate enabled: alembic version table added, database upgraded to current version.
#    b) auto-migrate disabled: fail with appropriate message.
#    """
#    def test_combined_database_automigrate(
#        self,
#        db_state3_combined,
#        metadata_state6_combined,
#        set_automigrate,
#    ):
#        db_url = db_state3_combined
#        with disposing_engine(db_state3_combined) as engine:
#            db = DatabaseVerifier(engine)
#            db.verify()
#            assert database_is_up_to_date(db_url, metadata_state6_combined)
#
#    def test_separate_databases_automigrate(
#        self,
#        db_state3_gxy,
#        db_state3_tsi,
#        metadata_state6_gxy,
#        metadata_state6_tsi,
#        set_automigrate,
#    ):
#        db1_url, db2_url = db_state3_gxy, db_state3_tsi
#        with disposing_engine(db1_url) as engine1, disposing_engine(db2_url) as engine2:
#            db = DatabaseVerifier(engine1, engine2)
#            db.verify()
#            assert database_is_up_to_date(db1_url, metadata_state6_gxy, GXY)
#            assert database_is_up_to_date(db2_url, metadata_state6_tsi, TSI)
#
#    def test_combined_database_no_automigrate(self, db_state3_combined):
#        with pytest.raises(OutdatedDatabaseError):
#            with disposing_engine(db_state3_combined) as engine:
#                db = DatabaseVerifier(engine)
#                db.verify()
#
#    def test_separate_databases_no_automigrate_gxy_raises_error(self, db_state3_gxy, db_state6_tsi):
#        with pytest.raises(OutdatedDatabaseError):
#            with disposing_engine(db_state3_gxy) as engine1, disposing_engine(db_state6_tsi) as engine2:
#                db = DatabaseVerifier(engine1, engine2)
#                db.verify()
#
#    def test_separate_databases_no_automigrate_tsi_raises_error(self, db_state6_gxy, db_state3_tsi):
#        with pytest.raises(OutdatedDatabaseError):
#            with disposing_engine(db_state6_gxy) as engine1, disposing_engine(db_state3_tsi) as engine2:
#                db = DatabaseVerifier(engine1, engine2)
#                db.verify()
#
#
#class TestDatabaseState4:
#    """
#    Initial state: non-empty database, SQLAlchemy Migrate version table present, Alembic version table present.
#    Oldest Alembic revision.
#    Expect:
#    a) auto-migrate enabled: database upgraded to current version.
#    b) auto-migrate disabled: fail with appropriate message.
#    """
#    def test_combined_database_automigrate(
#        self,
#        db_state4_combined,
#        metadata_state6_combined,
#        set_automigrate,
#    ):
#        db_url = db_state4_combined
#        with disposing_engine(db_url) as engine:
#            db = DatabaseVerifier(engine)
#            db.verify()
#            assert database_is_up_to_date(db_url, metadata_state6_combined)
#
#    def test_separate_databases_automigrate(
#        self,
#        db_state4_gxy,
#        db_state4_tsi,
#        metadata_state6_gxy,
#        metadata_state6_tsi,
#        set_automigrate,
#    ):
#        db1_url, db2_url = db_state4_gxy, db_state4_tsi
#        with disposing_engine(db1_url) as engine1, disposing_engine(db2_url) as engine2:
#            db = DatabaseVerifier(engine1, engine2)
#            db.verify()
#            assert database_is_up_to_date(db1_url, metadata_state6_gxy, GXY)
#            assert database_is_up_to_date(db2_url, metadata_state6_tsi, TSI)
#
#    def test_combined_database_no_automigrate(self, db_state4_combined):
#        with pytest.raises(OutdatedDatabaseError):
#            with disposing_engine(db_state4_combined) as engine:
#                db = DatabaseVerifier(engine)
#                db.verify()
#
#    def test_separate_databases_no_automigrate_gxy_raises_error(self, db_state4_gxy, db_state6_tsi):
#        with pytest.raises(OutdatedDatabaseError):
#            with disposing_engine(db_state4_gxy) as engine1, disposing_engine(db_state6_tsi) as engine2:
#                db = DatabaseVerifier(engine1, engine2)
#                db.verify()
#
#    def test_separate_databases_no_automigrate_tsi_raises_error(self, db_state6_gxy, db_state4_tsi):
#        with pytest.raises(OutdatedDatabaseError):
#            with disposing_engine(db_state6_gxy) as engine1, disposing_engine(db_state4_tsi) as engine2:
#                db = DatabaseVerifier(engine1, engine2)
#                db.verify()
#
#
#class TestDatabaseState5:
#    """
#    Initial state: non-empty database, Alembic version table present.
#    Oldest Alembic revision that does not include SQLAlchemy Migrate version table.
#    Expect:
#    a) auto-migrate enabled: database upgraded to current version.
#    b) auto-migrate disabled: fail with appropriate message.
#    """
#    def test_combined_database_automigrate(
#        self,
#        db_state5_combined,
#        metadata_state6_combined,
#        set_automigrate
#    ):
#        db_url = db_state5_combined
#        with disposing_engine(db_url) as engine:
#            db = DatabaseVerifier(engine)
#            db.verify()
#            assert database_is_up_to_date(db_url, metadata_state6_combined)
#
#    def test_separate_databases_automigrate(
#        self,
#        db_state5_gxy,
#        db_state5_tsi,
#        metadata_state6_gxy,
#        metadata_state6_tsi,
#        set_automigrate
#    ):
#        db1_url, db2_url = db_state5_gxy, db_state5_tsi
#        with disposing_engine(db1_url) as engine1, disposing_engine(db2_url) as engine2:
#            db = DatabaseVerifier(engine1, engine2)
#            db.verify()
#            assert database_is_up_to_date(db1_url, metadata_state6_gxy, GXY)
#            assert database_is_up_to_date(db2_url, metadata_state6_tsi, TSI)
#
#    def test_combined_database_no_automigrate(self, db_state5_combined):
#        with pytest.raises(OutdatedDatabaseError):
#            with disposing_engine(db_state5_combined) as engine:
#                db = DatabaseVerifier(engine)
#                db.verify()
#
#    def test_separate_databases_no_automigrate_gxy_raises_error(self, db_state5_gxy, db_state6_tsi):
#        with pytest.raises(OutdatedDatabaseError):
#            with disposing_engine(db_state5_gxy) as engine1, disposing_engine(db_state6_tsi) as engine2:
#                db = DatabaseVerifier(engine1, engine2)
#                db.verify()
#
#    def test_separate_databases_no_automigrate_tsi_raises_error(self, db_state6_gxy, db_state5_tsi):
#        with pytest.raises(OutdatedDatabaseError):
#            with disposing_engine(db_state6_gxy) as engine1, disposing_engine(db_state5_tsi) as engine2:
#                db = DatabaseVerifier(engine1, engine2)
#                db.verify()
#
#
#class TestDatabaseState6:
#    """
#    Initial state: non-empty database, Alembic version table present, database up-to-date.
#    Expect: do nothing.
#    """
#    def test_combined_database(self, db_state6_combined, metadata_state6_combined):
#        db_url = db_state6_combined
#        with disposing_engine(db_url) as engine:
#            db = DatabaseVerifier(engine)
#            db.verify()
#            assert database_is_up_to_date(db_url, metadata_state6_combined)
#
#    def test_separate_databases(
#        self,
#        db_state6_gxy,
#        db_state6_tsi,
#        metadata_state6_gxy,
#        metadata_state6_tsi
#    ):
#        db1_url, db2_url = db_state6_gxy, db_state6_tsi
#        with disposing_engine(db1_url) as engine1, disposing_engine(db2_url) as engine2:
#            db = DatabaseVerifier(engine1, engine2)
#            db.verify()
#            assert database_is_up_to_date(db1_url, metadata_state6_gxy, GXY)
#            assert database_is_up_to_date(db2_url, metadata_state6_tsi, TSI)
#
#
## Test helpers + their tests, misc. fixtures
#
#@pytest.fixture
#def set_automigrate(monkeypatch):
#    monkeypatch.setattr(DatabaseVerifier, '_is_automigrate_set', lambda _: True)
#
#
#@pytest.fixture(autouse=True)  # always override AlembicManager
#def set_alembic_manager(monkeypatch):
#    monkeypatch.setattr(
#        migrations, 'get_alembic_manager', lambda engine: AlembicManagerForTests(engine))
#
#
#@pytest.fixture(autouse=True)  # always override gxy_metadata
#def set_gxy_metadata(monkeypatch, metadata_state6_gxy):
#    monkeypatch.setattr(
#        migrations, 'get_gxy_metadata', lambda: metadata_state6_gxy)
#
#
#@pytest.fixture(autouse=True)  # always override tsi_metadata
#def set_tsi_metadata(monkeypatch, metadata_state6_tsi):
#    monkeypatch.setattr(
#        migrations, 'get_tsi_metadata', lambda: metadata_state6_tsi)
#
#
#class AlembicManagerForTests(AlembicManager):
#
#    def __init__(self, engine):
#        path1, path2 = self._get_paths_to_version_locations()
#        config_dict = {'version_locations': f'{path1};{path2}'}
#        super().__init__(engine, config_dict)
#
#    def _get_paths_to_version_locations(self):
#        # One does not simply use a relative path for both tests and package tests.
#        basepath = os.path.abspath(os.path.dirname(__file__))
#        basepath = os.path.join(basepath, 'versions')
#        path1 = os.path.join(basepath, 'db1')
#        path2 = os.path.join(basepath, 'db2')
#        return path1, path2
#
#
#def load_sqlalchemymigrate_version(db_url, version):
#    with disposing_engine(db_url) as engine:
#        with engine.connect() as conn:
#            sql_delete = f"delete from {SQLALCHEMYMIGRATE_TABLE}"  # there can be only 1 row
#            sql_insert = f"insert into {SQLALCHEMYMIGRATE_TABLE} values('_', '_', {version})"
#            conn.execute(sql_delete)
#            conn.execute(sql_insert)
#
#
#def test_load_sqlalchemymigrate_version(url_factory, metadata_state2_gxy):
#    db_url = url_factory()
#    with create_and_drop_database(db_url):
#        with disposing_engine(db_url) as engine:
#            load_metadata(metadata_state2_gxy, engine)
#            sql = f"select version from {SQLALCHEMYMIGRATE_TABLE}"
#            version = 42
#            with engine.connect() as conn:
#                result = conn.execute(sql).scalar()
#                assert result != version
#                load_sqlalchemymigrate_version(db_url, version)
#                result = conn.execute(sql).scalar()
#                assert result == version
#
#
#def database_is_up_to_date(db_url, current_state_metadata, model=None):
#    """
#    True if the database at `db_url` has the `current_state_metadata` loaded,
#    and is up-to-date (has most recent Alembic revision).
#
#    NOTE: Ideally, we'd determine the current metadata based on the model. However, since
#    metadata is a fixture, it cannot be called directly, and instead has to be
#    passed from the test as an argument. That's why we ensure that the passed
#    metadata is current (i.e., this guards againt an incorrect test).
#    """
#    # Ensure passed metatata is from a current state
#    metadata_tables = set(current_state_metadata.tables)
#    gxy_tables = {'gxy_table1', 'gxy_table2', 'gxy_table3'}
#    tsi_tables = {'tsi_table1', 'tsi_table2', 'tsi_table3'}
#    with disposing_engine(db_url) as engine:
#        am = AlembicManagerForTests(engine)
#
#        is_loaded = is_metadata_loaded(db_url, current_state_metadata)
#        is_gxy_subset = gxy_tables <= metadata_tables
#        is_tsi_subset = tsi_tables <= metadata_tables
#        if model == GXY:
#            return is_loaded and is_gxy_subset and am.is_up_to_date(GXY)
#        elif model == TSI:
#            return is_loaded and is_tsi_subset and am.is_up_to_date(TSI)
#        else:
#            return is_loaded and is_gxy_subset and is_tsi_subset and am.is_up_to_date(GXY) and am.is_up_to_date(TSI)
#
#
#def test_database_is_up_to_date(url_factory, metadata_state6_gxy):
#    db_url, metadata = url_factory(), metadata_state6_gxy
#    with create_and_drop_database(db_url):
#        with disposing_engine(db_url) as engine:
#            assert not database_is_up_to_date(db_url, metadata, GXY)
#            load_metadata(metadata, engine)
#            am = AlembicManagerForTests(engine)
#            am.stamp('heads')
#            assert database_is_up_to_date(db_url, metadata, GXY)
#
#
#def test_database_is_up_to_date_for_passed_model_only(url_factory, metadata_state6_gxy):
#    db_url, metadata = url_factory(), metadata_state6_gxy
#    with create_and_drop_database(db_url):
#        with disposing_engine(db_url) as engine:
#            assert not database_is_up_to_date(db_url, metadata, GXY)
#            assert not database_is_up_to_date(db_url, metadata, TSI)
#            load_metadata(metadata, engine)
#            am = AlembicManagerForTests(engine)
#            am.stamp('heads')
#            assert database_is_up_to_date(db_url, metadata, GXY)
#            assert not database_is_up_to_date(db_url, metadata, TSI)
#
#
#def test_database_is_up_to_date_checks_both_if_no_model_passed(url_factory, metadata_state6_combined):
#    db_url, metadata = url_factory(), metadata_state6_combined
#    with create_and_drop_database(db_url):
#        with disposing_engine(db_url) as engine:
#            assert not database_is_up_to_date(db_url, metadata)
#            load_metadata(metadata, engine)
#            am = AlembicManagerForTests(engine)
#            am.stamp('heads')
#            assert database_is_up_to_date(db_url, metadata)
#
#
#def test_database_is_not_up_to_date_if_noncurrent_metadata_passed(url_factory, metadata_state5_gxy):
#    db_url, metadata = url_factory(), metadata_state5_gxy
#    with create_and_drop_database(db_url):
#        with disposing_engine(db_url) as engine:
#            load_metadata(metadata, engine)
#            am = AlembicManagerForTests(engine)
#            am.stamp('heads')
#            assert not database_is_up_to_date(db_url, metadata, GXY)
#
#
#def test_database_is_not_up_to_date_if_metadata_not_loaded(url_factory, metadata_state6_gxy):
#    db_url, metadata = url_factory(), metadata_state6_gxy
#    with create_and_drop_database(db_url):
#        with disposing_engine(db_url) as engine:
#            am = AlembicManagerForTests(engine)
#            am.stamp('heads')
#            assert not database_is_up_to_date(db_url, metadata, GXY)
#
#
#def test_database_is_not_up_to_date_if_alembic_not_added(url_factory, metadata_state6_gxy):
#    db_url, metadata = url_factory(), metadata_state6_gxy
#    with create_and_drop_database(db_url):
#        with disposing_engine(db_url) as engine:
#            load_metadata(metadata, engine)
#            assert not database_is_up_to_date(db_url, metadata, GXY)
#
#
#def is_metadata_loaded(db_url, metadata):
#    """
#    True if the set of tables from the up-to-date state metadata (state6)
#    is a subset of the metadata reflected from `db_url`.
#    """
#    with disposing_engine(db_url) as engine:
#        with engine.connect() as conn:
#            db_metadata = MetaData()
#            db_metadata.reflect(bind=conn)
#            tables = _get_tablenames(metadata)
#            return set(tables) <= set(db_metadata.tables)
#
#
#def _get_tablenames(metadata):
#    metadata = listify(metadata)
#    tables = set()
#    for md in metadata:
#        tables |= set(md.tables)
#    return tables
#
#
#def test_is_metadata_loaded(url_factory, metadata_state1_gxy):
#    db_url, metadata = url_factory(), metadata_state1_gxy
#    with create_and_drop_database(db_url):
#        assert not is_metadata_loaded(db_url, metadata)
#        with disposing_engine(db_url) as engine:
#            with engine.connect() as conn:
#                metadata.create_all(bind=conn)
#        assert is_metadata_loaded(db_url, metadata)
#
#
#def test_is_multiple_metadata_loaded(url_factory, metadata_state1_gxy, metadata_state1_tsi):
#    db_url = url_factory()
#    metadata = [metadata_state1_gxy, metadata_state1_tsi]
#    with create_and_drop_database(db_url):
#        assert not is_metadata_loaded(db_url, metadata)
#        with disposing_engine(db_url) as engine:
#            with engine.connect() as conn:
#                metadata_state1_gxy.create_all(bind=conn)
#                metadata_state1_tsi.create_all(bind=conn)
#        assert is_metadata_loaded(db_url, metadata)
#
#
#def test_load_metadata(url_factory, metadata_state1_gxy):
#    db_url, metadata = url_factory(), metadata_state1_gxy
#    with create_and_drop_database(db_url):
#        with disposing_engine(db_url) as engine:
#            assert not is_metadata_loaded(db_url, metadata)
#            load_metadata(metadata, engine)
#            assert is_metadata_loaded(db_url, metadata)
#
#
#"""
## Fixtures: databases loaded with a given state.
#Each state has 3 versions: gxy, tsi, combined (see fixtures/schemas.py)
#
#Each fixture is constructed as follows:
#1. Create a new sqlite database url.
#2. Pass database url with state metadata fixture to a `_setup_db_url_state{state#}` function.
#3. Inside the function, create database and load any state-specific data.
#"""
#
#
## state 1
#@pytest.fixture
#def db_state1_gxy(url_factory, metadata_state1_gxy):
#    yield from _setup_db_state1(url_factory(), metadata_state1_gxy)
#
#
#@pytest.fixture
#def db_state1_tsi(url_factory, metadata_state1_tsi):
#    yield from _setup_db_state1(url_factory(), metadata_state1_tsi)
#
#
#@pytest.fixture
#def db_state1_combined(url_factory, metadata_state1_combined):
#    yield from _setup_db_state1(url_factory(), metadata_state1_combined)
#
#
#def _setup_db_state1(db_url, metadata):
#    with create_and_drop_database(db_url):
#        with disposing_engine(db_url) as engine:
#            load_metadata(metadata, engine)
#            yield db_url
#
#
## state 2
#@pytest.fixture
#def db_state2_gxy(url_factory, metadata_state2_gxy):
#    yield from _setup_db_state2(url_factory(), metadata_state2_gxy)
#
#
#@pytest.fixture
#def db_state2_tsi(url_factory, metadata_state2_tsi):
#    yield from _setup_db_state2(url_factory(), metadata_state2_tsi)
#
#
#@pytest.fixture
#def db_state2_combined(url_factory, metadata_state2_combined):
#    yield from _setup_db_state2(url_factory(), metadata_state2_combined)
#
#
#def _setup_db_state2(db_url, metadata):
#    with create_and_drop_database(db_url):
#        with disposing_engine(db_url) as engine:
#            load_metadata(metadata, engine)
#            yield db_url
#
#
## state 3
#@pytest.fixture
#def db_state3_gxy(url_factory, metadata_state3_gxy):
#    yield from _setup_db_state3(url_factory(), metadata_state3_gxy)
#
#
#@pytest.fixture
#def db_state3_tsi(url_factory, metadata_state3_tsi):
#    yield from _setup_db_state3(url_factory(), metadata_state3_tsi)
#
#
#@pytest.fixture
#def db_state3_combined(url_factory, metadata_state3_combined):
#    yield from _setup_db_state3(url_factory(), metadata_state3_combined)
#
#
#def _setup_db_state3(db_url, metadata):
#    with create_and_drop_database(db_url):
#        with disposing_engine(db_url) as engine:
#            load_metadata(metadata, engine)
#            load_sqlalchemymigrate_version(db_url, SQLALCHEMYMIGRATE_LAST_VERSION)
#            yield db_url
#
#
## state 4
#@pytest.fixture
#def db_state4_gxy(url_factory, metadata_state4_gxy):
#    yield from _setup_db_state4(url_factory(), metadata_state4_gxy, GXY)
#
#
#@pytest.fixture
#def db_state4_tsi(url_factory, metadata_state4_tsi):
#    yield from _setup_db_state4(url_factory(), metadata_state4_tsi, TSI)
#
#
#@pytest.fixture
#def db_state4_combined(url_factory, metadata_state4_combined):
#    yield from _setup_db_state4(url_factory(), metadata_state4_combined)
#
#
#def _setup_db_state4(db_url, metadata, model=None):
#    with create_and_drop_database(db_url):
#        with disposing_engine(db_url) as engine:
#            load_metadata(metadata, engine)
#            load_sqlalchemymigrate_version(db_url, SQLALCHEMYMIGRATE_LAST_VERSION)
#
#            revisions: Union[str, list]
#            if model == GXY:
#                revisions = GXY_REVISION_0
#            elif model == TSI:
#                revisions = TSI_REVISION_0
#            else:
#                revisions = [GXY_REVISION_0, TSI_REVISION_0]
#            am = AlembicManagerForTests(engine)
#            am.stamp(revisions)
#
#            yield db_url
#
#
## state 5
#@pytest.fixture
#def db_state5_gxy(url_factory, metadata_state5_gxy):
#    yield from _setup_db_state5(url_factory(), metadata_state5_gxy, GXY)
#
#
#@pytest.fixture
#def db_state5_tsi(url_factory, metadata_state5_tsi):
#    yield from _setup_db_state5(url_factory(), metadata_state5_tsi, TSI)
#
#
#@pytest.fixture
#def db_state5_combined(url_factory, metadata_state5_combined):
#    yield from _setup_db_state5(url_factory(), metadata_state5_combined)
#
#
#def _setup_db_state5(db_url, metadata, model=None):
#    with create_and_drop_database(db_url):
#        with disposing_engine(db_url) as engine:
#            load_metadata(metadata, engine)
#
#            revisions: Union[str, list]
#            if model == GXY:
#                revisions = GXY_REVISION_1
#            elif model == TSI:
#                revisions = TSI_REVISION_1
#            else:
#                revisions = [GXY_REVISION_1, TSI_REVISION_1]
#            am = AlembicManagerForTests(engine)
#            am.stamp(revisions)
#
#            yield db_url
#
#
## state 6
#@pytest.fixture
#def db_state6_gxy(url_factory, metadata_state6_gxy):
#    yield from _setup_db_state6(url_factory(), metadata_state6_gxy, GXY)
#
#
#@pytest.fixture
#def db_state6_tsi(url_factory, metadata_state6_tsi):
#    yield from _setup_db_state6(url_factory(), metadata_state6_tsi, TSI)
#
#
#@pytest.fixture
#def db_state6_combined(url_factory, metadata_state6_combined):
#    yield from _setup_db_state6(url_factory(), metadata_state6_combined)
#
#
#def _setup_db_state6(db_url, metadata, model=None):
#    with create_and_drop_database(db_url):
#        with disposing_engine(db_url) as engine:
#            load_metadata(metadata, engine)
#
#            revisions: Union[str, list]
#            if model == GXY:
#                revisions = GXY_REVISION_2
#            elif model == TSI:
#                revisions = TSI_REVISION_2
#            else:
#                revisions = [GXY_REVISION_2, TSI_REVISION_2]
#            am = AlembicManagerForTests(engine)
#            am.stamp(revisions)
#
#            yield db_url
