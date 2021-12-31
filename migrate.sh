#!/bin/sh

#######
# We use branch labels to distinguish between the galaxy and the tool_shed_install models,
# so in most cases you'll need to identify the branch to which your command should be applied.
# Use these identifiers: `gxy` for galaxy, and `tsi` for tool_shed_install.
#
# To create a revision for galaxy:
# ./migrate.sh revision --head=gxy@head -m "your description"
#
# To create a revision for tool_shed_install:
# ./migrate.sh revision --head=tsi@head -m "your description"
#
# To upgrade:
# ./migrate.sh upgrade gxy@head  # upgrade gxy to head revision
# ./migrate.sh upgrade gxy@+1  # upgrade gxy to 1 revision above current
# ./migrate.sh upgrade [revision identifier]  # upgrade gxy to a specific revision
# ./migrate.sh upgrade [revision identifier]+1  # upgrade gxy to 1 revision above specific revision
# ./migrate.sh upgrade heads  # upgrade gxy and tsi to head revisions
#
# To downgrade:
# ./migrate.sh downgrade gxy@base  # downgrade gxy to base (empty db with empty alembic table)
# ./migrate.sh downgrade gxy@-1  # downgrade gxy to 1 revision below current
# ./migrate.sh downgrade [revision identifier]  # downgrade gxy to a specific revision
# ./migrate.sh downgrade [revision identifier]-1  # downgrade gxy to 1 revision below specific revision
#
# To pass a galaxy config file, use `--galaxy-config`
#
# You may also override the gxy database url and/or the tsi database url with env vars:
# GALAXY_CONFIG_OVERRIDE_DATABASE_CONNECTION=my-db-url ./migrate.sh ...
# GALAXY_INSTALL_CONFIG_OVERRIDE_DATABASE_CONNECTION=my-other-db-url ./migrate.sh ...
#
# For more options, see Alembic's documentation at https://alembic.sqlalchemy.org
#######

ALEMBIC_CONFIG='lib/galaxy/model/migrations/alembic.ini'

cd `dirname $0`

. ./scripts/common_startup_functions.sh

setup_python

find lib/galaxy/model/migrations/alembic -name '*.pyc' -delete
python ./scripts/migrate_db.py --config "$ALEMBIC_CONFIG" "$@"
