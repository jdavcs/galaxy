import logging
import os.path
import sys

from alembic import context
from alembic import config
from alembic.config import main

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'lib')))

from galaxy.model.orm.scripts import get_config

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


# TODO this is all a draft
def invoke_alembic_main():
    # Migrate has its own args, so cannot use argparse
    galaxy_config = get_config(sys.argv, use_argparse=False, cwd=os.getcwd())

    gxy_url = galaxy_config['db_url']
    tsi_url = galaxy_config['install_database_connection']

    alembic_config_file = '/home/sergey/0dev/galaxy/_galaxy/dev/lib/galaxy/model/migrations/alembic.ini'

    #breakpoint()
    config.config_file_name = alembic_config_file
    cfg = config.Config(alembic_config_file)
   #  cfg.attributes['sqlalchemy.url'] = gxy_url

    # set alembic config file
    # get branch?
    # set url based on branch
    # how do we pass an argument here??????

    #main(alembic_config_file)

    breakpoint()



# all command args are passed via $@ from manage_db.sh
if __name__ == "__main__":
    invoke_alembic_main()
