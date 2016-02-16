#!/bin/bash

# docker build -t whille/sym_sync .
# docker tag whille/sym_sync 123.59.14.139:5000/kingfile/sym_sync

DST_IP=192.168.138.231
SRC_DIR=/caches
VOLUME=${SRC_DIR}

CONTAINER_PREFIX="kfile_"
CONTAINER_DATA_NAME=${CONTAINER_PREFIX}"data"

docker run -d --name sym_sync \
    --volumes-from ${CONTAINER_DATA_NAME} \
    -e DST_IP=${DST_IP} \
    -e OWNER=2048 -e GROUP=2048 \
    -p 10873:873 \
    whille/sym_sync

# dexec sym_sync /usr/local/bin/start_lsync.sh
