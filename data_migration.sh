#!/bin/bash
folder=$1
dbname=$2

for entry in "$folder"/*.sql
do
    if [ ${#dbname} -gt 0 ]; then
        psql -f $entry --dbname $2
    else
        psql -f $entry
    fi
done
