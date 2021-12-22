#!/bin/sh

# this is all wrong now
# TODO: Add detailed instructions here + link to relevant alembic docs

cd `dirname $0`

. ./scripts/common_startup_functions.sh

setup_python

#find lib/galaxy/model/migrate/versions -name '*.pyc' -delete
#python ./scripts/manage_db.py $@

python ./scripts/manage_alembic_db.py $@
