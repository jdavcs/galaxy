#!/bin/sh

# Use this script to create and initialize a new tool_shed database.

cd "$(dirname "$0")"

. ./scripts/common_startup_functions.sh

setup_python

python ./scripts/create_ts_db.py "$@" tool_shed

