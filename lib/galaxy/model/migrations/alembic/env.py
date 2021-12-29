import re

from alembic import context
from alembic import script
from sqlalchemy import engine_from_config
from sqlalchemy import pool, create_engine

# TODO make this conditional
import sys
import os


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
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
    'tsi': 'sqlite:////home/sergey/0dev/galaxy/_galaxy/dev/database/installuniverse.sqlite?isolation_level=IMMEDIATE',
}

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


def _get_migration_urls():
    urls = URLS
    migration_urls = []

    revision_str = config.cmd_opts.revision
    if revision_str == 'heads' or revision_str == 'base':   # TODO what about "downgrade -1"?
        migration_urls = (urls['gxy'], urls['tsi'])
        #raise # TODO: run for each url. Verify that this is correct
    elif revision_str.startswith('-') and config.cmd_opts.fn.__name__ == 'downgrade':
        migration_urls = (urls['gxy'], urls['tsi'])
        raise # TODO: run for each url. Verify that this is correct
    elif revision_str.startswith('gxy@'):
        migration_urls = (urls['gxy'],)
    elif revision_str.startswith('tsi@'):
        migration_urls = (urls['tsi'],)
    else:
        revision_id = context.get_revision_argument()
        script_directory = script.ScriptDirectory.from_config(config)
        revision = script_directory.get_revision(revision_id)
        if not revision:
            raise Exception('Revision not found')  # TODO: more specific error?
        if 'gxy' in revision.branch_labels:
            migration_urls = (urls['gxy'],)
        elif 'tsi' in revision.branch_labels:
            migration_urls = (urls['tsi'],)

    #breakpoint()
    return migration_urls   



if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()






def _get_db_url():
    raise
    # TODO see this sample logic:
    if 'current' in sys.argv:
        print('current: run for both')
    else:
        revision_arg = context.get_revision_argument()  # TODO can be a tuple or none
        if revision_arg is None:
            print('base? what do we do here?')
        elif type(revision_arg) is tuple:
            print('heads: run for both')
        elif '+' in revision_arg or '-' in revision_arg:
            print('relative migration. use sys.argv to get the branch label')
        else:
            print('we might have a rev. try to get it; if yes - get branch, then engine. done. Else: raise error')

        foo = context.get_revision_argument()

    if not context.get_x_argument():  # called not from script
        return config.get_main_option("sqlalchemy.url")

    script_directory = script.ScriptDirectory.from_config(config)
    revision_arg = context.get_revision_argument()  # TODO can be a tuple or none

    if type(revision_arg) is tuple:  # probably heads?
        # loop over both!
        pass

    if not revision_arg:  # assume base???

        raise Exception('No revision supplied')  # TODO handle tuple or None?

    revision = script_directory.get_revision(revision_str)  # TODO if using relative syntax, this breaks: i.e., "head-1" is not a revision id
    if not revision:
        raise Exception('Revision not found')  # TODO do i need to handle this?

    gxy_url = context.get_x_argument(as_dictionary=True).get('gxy_url')
    tsi_url = context.get_x_argument(as_dictionary=True).get('tsi_url')

    # TODO: export these, don't duplicate
    if 'gxy' in revision.branch_labels:
        return gxy_url
    elif 'tsi' in revision.branch_labels:
        return tsi_url

    #breakpoint()
    #urls = _get_urls()

    #engines = {}
    #for name, url in urls.items():
    #    engines[name] = record = {}
    #    record['engine'] = create_engine(url)

    #for name, record in engines.items():
    #    engine = record['engine']
    #    record['connection'] = conn = engine.connect()  # TODO: do not connect if it's the same engine!!!
    #    record['transaction'] = conn.begin()

    #try:
    #    for name, record in engines.items():
    #        # TODO log maybe?  logger.info("Migrating database %s" % name)
    #        context.configure(
    #            connection=conn, target_metadata=target_metadata
    #        )
    #        print('calling for ', name )
    #        #context.run_migrations()
    #        #context.run_migrations(engine_name=name)  # kwds are passed to upgrade/downgrade (see template in maco file)

    #    for name, record in engines.items():
    #        record["transaction"].commit()
    #except:
    #    for record in engines.values():
    #        record["transaction"].rollback()
    #    raise
    #finally:
    #    for record in engines.values():
    #        record["connection"].close()



    #raise # not ready
    #url = _get_db_url()
    #connectable = create_engine(url)

    ##connectable = engine_from_config(
    ##    config.get_section(config.config_ini_section),
    ##    prefix="sqlalchemy.",
    ##    poolclass=pool.NullPool,
    ##)

    #with connectable.connect() as connection:
    #    context.configure(
    #        connection=connection, target_metadata=target_metadata
    #    )

    #    with context.begin_transaction():
    #        context.run_migrations()

