import re

from alembic import context
from alembic import script
from sqlalchemy import engine_from_config
from sqlalchemy import pool, create_engine


config = context.config

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None  # TODO need this for reflection (not critical for prototype)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# TODO: this should come from galaxy's config, or at least from the x arg
URLS = {
    'gxy': 'sqlite:////home/sergey/0dev/galaxy/_galaxy/dev/database/universe.sqlite?isolation_level=IMMEDIATE',
   # 'tsi': 'sqlite:////home/sergey/0dev/galaxy/_galaxy/dev/database/universe.sqlite?isolation_level=IMMEDIATE',
    'tsi': 'sqlite:////home/sergey/0dev/galaxy/_galaxy/dev/database/installuniverse.sqlite?isolation_level=IMMEDIATE',
}

#URLS = {
#    'gxy': 'postgresql://galaxy:42@localhost/alembic_gxy',
#    'tsi': 'postgresql://galaxy:42@localhost/alembic_tsi',
#}

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    if not config.cmd_opts:
        _run_migrations_offline_programmatic()
    else:
        _run_migrations_offline_script()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    if not config.cmd_opts:
        _run_migrations_online_programmatic()
    else:
        _run_migrations_online_script()


def _run_migrations_online_programmatic():
    # invoked programmatically
    url = config.get_main_option("sqlalchemy.url")
    engine = create_engine(url)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()  # TODO make sure this doesn't break things


def _run_migrations_online_script():
    # invoked via script
    print('MY DEBUG: Running migrations ONLINE, invoked via script')
    cmd_name = config.cmd_opts.cmd[0].__name__

    if cmd_name == 'current':
        for url in URLS.values():
            engine = create_engine(url)
            with engine.connect() as connection:
                context.configure(connection=connection, target_metadata=target_metadata)
                with context.begin_transaction():
                    context.run_migrations()
            engine.dispose()  # TODO make sure this doesn't break things
        return  # we're done

    assert cmd_name in ('upgrade', 'downgrade')  # sanity check

    revision_str = config.cmd_opts.revision

    if revision_str.startswith('gxy@'):  # gxy label followed by anything
        url = URLS['gxy']
    elif revision_str.startswith('tsi@'):  # tsi label followed by anything
        url = URLS['tsi']
    else:
        p = re.compile('([0-9A-Fa-f]+)([+-]\d)?')  # matches a full or partial revision id, or a relative migration identifier
        m = p.match(revision_str)
        if not m:
            raise Exception('invalid revision identifier')  # TODO edit error message
        revision_id = m.group(1)

        script_directory = script.ScriptDirectory.from_config(config)
        revision = script_directory.get_revision(revision_id)
        if not revision:
            raise Exception('Revision not found')  # TODO: more specific error?
        if 'gxy' in revision.branch_labels:
            url = URLS['gxy']
        elif 'tsi' in revision.branch_labels:
            url = URLS['tsi']

    engine = create_engine(url)
    with engine.connect() as conn:
        context.configure(connection=conn, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()


def _run_migrations_offline_programmatic():
    # invoked programmatically
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def _run_migrations_offline_script():
    # invoked via script
    print('MY DEBUG: Running migrations OFFLINE, invoked via script')

    cmd_name = config.cmd_opts.cmd[0].__name__

    if cmd_name == 'current':
        for url in URLS.values():
            engine = create_engine(url)
            with engine.connect() as connection:
                context.configure(connection=connection, target_metadata=target_metadata)
                with context.begin_transaction():
                    context.run_migrations()
            engine.dispose()  # TODO make sure this doesn't break things
        return  # we're done

    assert cmd_name in ('upgrade', 'downgrade')  # sanity check

    revision_str = config.cmd_opts.revision

    if revision_str.startswith('gxy@'):  # gxy label followed by anything
        url = URLS['gxy']
    elif revision_str.startswith('tsi@'):  # tsi label followed by anything
        url = URLS['tsi']
    else:
        p = re.compile('([0-9A-Fa-f]+)([+-]\d)?')  # matches a full or partial revision id, or a relative migration identifier
        m = p.match(revision_str)
        if not m:
            raise Exception('invalid revision identifier')  # TODO edit error message
        revision_id = m.group(1)

        script_directory = script.ScriptDirectory.from_config(config)
        revision = script_directory.get_revision(revision_id)
        if not revision:
            raise Exception('Revision not found')  # TODO: more specific error?
        if 'gxy' in revision.branch_labels:
            url = URLS['gxy']
        elif 'tsi' in revision.branch_labels:
            url = URLS['tsi']

    context.configure(
        url=url,
        target_metadata=target_metadata,  # TODO we can fix this
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
