#!/bin/bash


DBNAME="deshimemedb"
DBUSER="werconcitus"
DBPASS="dmconcitus666"


OS="$(uname -s)"


if [ $OS == "Darwin" ]; then
    psql -d postgres --command "CREATE USER $DBUSER WITH SUPERUSER PASSWORD '$DBPASS';" && createdb -O $DBUSER $DBNAME
else
sudo -u postgres bash << EOF
    psql --command "CREATE USER $DBUSER WITH SUPERUSER PASSWORD '$DBPASS';" && createdb -O $DBUSER $DBNAME
EOF
fi