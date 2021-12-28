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

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def invoke_alembic():
    galaxy_config = GalaxyAppConfiguration()
    db_url = galaxy_config.database_connection
    install_db_url = galaxy_config.install_database_connection or db_url  # TODO remove duplication w/config
    _insert_x_argument('tsi_url', install_db_url)
    _insert_x_argument('gxy_url', db_url)
    alembic.config.main()


def _insert_x_argument(key, value):
    # `_insert_x_argument('mykey', 'myval')` transforms `foo -a 1` into `foo -x mykey=myval -a 42`
    sys.argv.insert(1, f'{key}={value}')
    sys.argv.insert(1, '-x')



if __name__ == '__main__':
    invoke_alembic()
