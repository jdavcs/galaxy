import logging 

from sqlalchemy import create_engine, MetaData, Table

from alembic import command
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory

log = logging.getLogger(__name__)

ALEMBIC_TABLE = 'alembic_version'
COLUMN_ATTRIBUTES_TO_VERIFY = ('name', 'key', 'primary_key', 'nullable', 'default')
TYPE_ATTRIBUTES_TO_VERIFY = ('length',)

class DBManager:

    def __init__(self, url, metadata):
        self.url = url
        self.metadata = metadata        # loaded from module
        self.db_metadata = MetaData()   # loaded from database
        self.engine = create_engine(url)
        with self.engine.connect() as conn:
            self._load_db_metadata(conn)

    def is_initialized(self):
        """Assume database is initialized if 'dataset' table exists."""
        return 'dataset' in self.db_metadata.tables

    def is_alembic_versioned(self):
        """Database is under Alembic version control if 'alembic_version' table exists."""
        return 'alembic_version' in self.db_metadata.tables

    def is_migrate_versioned(self):
        """Database is under SQLAlchemy version control if 'migrate_version' table exists."""
        return 'migrate_version' in self.db_metadata.tables

    def is_current(self):
        cfg = Config()
        cfg.set_main_option('script_location', 'lib/galaxy/model/migrations/alembic') #TODO remove duplication
        cfg.set_main_option('sqlalchemy.url', self.url)
        script = ScriptDirectory.from_config(cfg)
        app_version = script.get_current_head()
        with self.engine.connect() as conn:
            context = MigrationContext.configure(conn)
            db_version = context.get_current_revision()
        return db_version == app_version

    def initialize_schema(self):
        log.info('Initializing database schema')
        with self.engine.connect() as conn:
            self.metadata.bind = conn
            self.metadata.create_all()
            self._load_db_metadata(conn)

    def initialize_alembic(self):

        log.info('Placing database under Alembic version control')
        cfg = Config()
        cfg.set_main_option('script_location', 'lib/galaxy/model/migrations/alembic') #TODO fix path creation!
        cfg.set_main_option('sqlalchemy.url', self.url)
        command.stamp(cfg, "head")  # create alembic_version table in db; insert latest (head) revision id.

    def _load_db_metadata(self, conn):
        self.db_metadata.bind = conn  
        self.db_metadata.reflect()
 

class MetaDataComparator:
    # TODO: can we replace this with a library?
    """Compares 2 SQLAlchemy MetaData objects."""
    def _exclude_alembic(self, metadata):
        return [table for table in metadata.sorted_tables if table.name != ALEMBIC_TABLE]

    def compare(self, metadata1, metadata2, column_attributes, type_attributes=None):
        tables1, tables2 = self._exclude_alembic(metadata1), self._exclude_alembic(metadata2)
        assert len(tables1) == len(tables2), 'Number of tables not the same'

        for (t1, t2) in zip(tables1, tables2):
            self.compare_indexes(t1, t2)
            assert len(t1.columns) == len(t2.columns), 'Different number of columns in table %s' % t1.name
            for (c1, c2) in zip(t1.columns, t2.columns):
                self.compare_types(c1, c2, type_attributes)
                self.compare_foreignkeys(c1, c2)
                self.compare_column_attributes(c1, c2, column_attributes)

    def compare_indexes(self, table1, table2):
        assert len(table1.indexes) ==  len(table2.indexes), 'Different number of indexes on table %s' % table1.name
        indexes1 = {i.name: i for i in table1.indexes} # TODO no need? just define a sort key?
        indexes2 = {i.name: i for i in table2.indexes}
        for (name1, name2) in zip(sorted(indexes1), sorted(indexes2)):
            assert name1 == name2, 'Different index names'
            assert indexes1[name1].unique == indexes2[name2].unique
            for (c1, c2) in zip(indexes1[name1].columns, indexes2[name2].columns):
                assert c1.name == c2.name

    def compare_types(self, column1, column2, type_attributes=None):
        type1, type2 = column1.type, column2.type
        assert isinstance(column1.type, type(type2)) or isinstance(column2.type, type(type1)), \
            'Different types on column %s: %s, %s' % (column1.name, type1, type2)
        if type_attributes:
            for key in type_attributes:
                if hasattr(type1, key) or hasattr(type2, key):
                    assert getattr(type1, key) == getattr(type2, key), \
                        "Type %s attributes don't match on attribute %s " % (type1, key)

    def compare_column_attributes(self, column1, column2, column_attributes):
        for key in column_attributes:
            attr1, attr2 = getattr(column1, key), getattr(column2, key)
            assert hasattr(attr1, 'arg') == hasattr(attr2, 'arg')
            if not hasattr(attr1, 'arg'):
                assert attr1 == attr2
            else:
                assert attr1.is_callable == attr2.is_callable
                if attr1.is_callable:
                    assert attr1.arg.__name__ == attr2.arg.__name__
                else:
                    assert attr1.arg == attr2.arg

    def compare_foreignkeys(self, c1, c2):
        assert len(c1.foreign_keys) == len(c2.foreign_keys)
        for (fk1, fk2) in zip(c1.foreign_keys, c2.foreign_keys):
            assert fk1.column.name == fk2.column.name
            assert fk1.column.table.name == fk2.column.table.name
            assert fk1.onupdate == fk2.onupdate
            assert fk1.ondelete == fk2.ondelete
