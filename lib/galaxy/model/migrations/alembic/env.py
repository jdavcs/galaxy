import re

from alembic import context
from alembic import script
from sqlalchemy import engine_from_config
from sqlalchemy import pool, create_engine

from galaxy.config import GalaxyAppConfiguration
from galaxy.model.migrations import GXY, TSI

config = context.config
target_metadata = None  # Not implemented: used for autogenerate, which we don't use here.

galaxy_config = GalaxyAppConfiguration()
URLS = {
    GXY: galaxy_config.database_connection,
    TSI: galaxy_config.install_database_connection or galaxy_config.database_connection,
}


def run_migrations_offline():
    """Run migrations in offline mode; database url required."""
    if not config.cmd_opts:
        _run_migrations_offline_programmatic()
    else:
        _run_migrations_offline_script()


def run_migrations_online():
    """Run migrations in online mode: engine and connection required."""
    if not config.cmd_opts:
        _run_migrations_online_programmatic()
    else:
        _run_migrations_online_script()


def _run_migrations_online_programmatic():
    # Invoked programmatically
    url = config.get_main_option("sqlalchemy.url")

    engine = create_engine(url)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()


def _run_migrations_online_script():
    # Invoked via script
    print('MY DEBUG: Running migrations ONLINE, invoked via script')
    cmd_name = config.cmd_opts.cmd[0].__name__

    if cmd_name == 'current':
        for url in URLS.values():

            engine = create_engine(url)
            with engine.connect() as connection:
                context.configure(connection=connection, target_metadata=target_metadata)
                with context.begin_transaction():
                    context.run_migrations()
            engine.dispose()

        return

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



def _configure_and_run_migrations_offline(url):
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def _run_migrations_offline_programmatic():
    # Invoked programmatically
    url = config.get_main_option("sqlalchemy.url")
    _configure_and_run_migrations_offline(url)


def _run_migrations_offline_script():
    # Invoked via script
    print('MY DEBUG: Running migrations OFFLINE, invoked via script')

    cmd_name = config.cmd_opts.cmd[0].__name__

    if cmd_name == 'current':
        for url in URLS.values():
            _configure_and_run_migrations_offline(url)
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

    _configure_and_run_migrations_offline(url)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
