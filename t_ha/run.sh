#!/bin/bash

CUR_DIR=$(dirname $(readlink -f $(ls $0)))

docker run \
    --privileged=true \
    -v /dev:/dev -v /lib/modules:/lib/modules \
    --cap-add=NET_ADMIN --net=host \
    -e ROLE=BACKUP \
    -e PEER_IP=192.168.140.148 \
    -e VIP=192.168.140.250 \
    --name=redis_ha \
    -d redis_ha
