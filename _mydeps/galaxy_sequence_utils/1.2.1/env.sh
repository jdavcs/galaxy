#!/bin/sh

# add path to executable called by tool: gx-fastq-groomer
PATH=/home/sergey/0dev/galaxy/tooldev/bin/:$PATH
export PATH

# add path to sequence_utils package w/python modules
PYTHONPATH="/home/sergey/0dev/galaxy/tooldev/sequence_utils/:$PYTHONPATH"
export PYTHONPATH
