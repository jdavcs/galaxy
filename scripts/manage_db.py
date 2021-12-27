""" 
TODO: add description
"""
import logging
import os.path
import sys

import alembic.config

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'lib')))

from galaxy.config import GalaxyAppConfiguration
from galaxy.model.orm.scripts import get_config

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def invoke_alembic():
    galaxy_config = GalaxyAppConfiguration()
    db_url = galaxy_config.database_connection
    install_db_url = galaxy_config.install_database_connection
    sys.argv.insert(1, f'tsi_url={install_db_url}')
    sys.argv.insert(1, '-x')
    sys.argv.insert(1, f'gxy_url={db_url}')
    sys.argv.insert(1, '-x')
    alembic.config.main()


if __name__ == '__main__':
    invoke_alembic()
