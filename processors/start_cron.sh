#!/bin/bash

DIR=`dirname "$(readlink -f "$0")"`
BASE_DIR=$DIR/..

# Activate the virtual environment
cd $BASE_DIR
source env/bin/activate
exec python $DIR/cron.py