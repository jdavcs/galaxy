#TODO: add description
""" 
TODO: add description
"""
import logging
import os.path
import sys

import alembic.config

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'lib')))

from galaxy.config import GalaxyAppConfiguration
from galaxy.model.migrations import GXY, TSI

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def invoke_alembic():
    _add_db_urls_to_command_arguments()

    # Accept 'heads' as the target revision argument to enable upgrading both gxy and tsi in one command.
    # This is consistent with Alembic's CLI, which allows `upgrade heads`. However, this would not work for
    # separate gxy and tsi databases: we can't attach a database url to a revision after Alembic has been
    # invoked with the 'upgrade' command and the 'heads' argument. So, instead we invoke Alembic for each head.
    if 'heads' in sys.argv and 'upgrade' in sys.argv:
        i = sys.argv.index('heads')
        sys.argv[i] = f'{GXY}@head'
        alembic.config.main()
        sys.argv[i] = f'{TSI}@head'
        alembic.config.main()
    else:
        alembic.config.main()


def _add_db_urls_to_command_arguments():
    galaxy_config = GalaxyAppConfiguration()
    db_url = galaxy_config.database_connection
    install_db_url = galaxy_config.install_database_connection or db_url  # TODO remove duplication w/config
    _insert_x_argument('tsi_url', install_db_url)
    _insert_x_argument('gxy_url', db_url)


def _insert_x_argument(key, value):
    # `_insert_x_argument('mykey', 'myval')` transforms `foo -a 1` into `foo -x mykey=myval -a 42`
    sys.argv.insert(1, f'{key}={value}')
    sys.argv.insert(1, '-x')


if __name__ == '__main__':
    invoke_alembic()
