#!/bin/bash

function start_tfreg {
    docker build . -t "rnrtfreg:local"
    echo "running tfreg container"
    docker run -d --rm \
        --name tfreg \
        --link psqldb:psqldb \
        -e "TF_REG_SQL_SERVER_CONNECTION_STRING=postgresql://rnrtfreg:rnrtfreg@psqldb/rnrtfreg" \
        -p 8443:8443 \
        rnrtfreg:local
}


function start_psql {
    echo "running psql container"
    docker run -d --rm \
        --name psqldb \
        -e "POSTGRES_PASSWORD=rnrtfreg" \
        -e "POSTGRES_USER=rnrtfreg" \
        -e "POSTGRES_DB: rnrtfreg" \
        -e PGDATA=/var/lib/postgresql/data/pgdata \
        -v $PWD/tmp/psql:/var/lib/postgresql/data \
        -p 5432:5432 \
        postgres:15.3-alpine3.18 
}

start_psql
start_tfreg

old=$(shasum ./app/* | shasum -t)

while true
do
    new=$(shasum ./app/* | shasum -t)

    if ! [ "$old" = "$new" ]
    then
        echo "files has changes reloading"
        docker stop tfreg
        start_tfreg
        old=$(shasum ./app/* | shasum -t)
    fi

    sleep 1
done