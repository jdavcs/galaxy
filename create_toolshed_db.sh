#!/bin/sh

#######
# Use this script to create and initialize a new Tool Shed database.
#
# (Use create_db.sh to create and initialize a new Galaxy or
# Tool Shed Install database.)
#######

cd "$(dirname "$0")"

. ./scripts/common_startup_functions.sh

setup_python

python ./scripts/create_toolshed_db.py "$@" tool_shed

