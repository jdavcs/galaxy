#!/bin/sh

#######
# Use this script to manage Tool Shed migrations.
# Use migrate.sh to manage Galaxy and Tool Shed Install migrations.
#
# To downgrade to a specific version, use something like:
# sh manage_db.sh downgrade --version=3 tool_shed
#######

cd `dirname $0`

. ./scripts/common_startup_functions.sh

setup_python

find lib/galaxy/model/migrate/versions -name '*.pyc' -delete
python ./scripts/manage_db.py $@
