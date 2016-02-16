#!/bin/bash

DELAY=${DELAY:-5}
DST_IP=${DST_IP:-localhost}

lsyncd --nodaemon -delay ${DELAY} \
    -rsync /caches   rsync://${DST_IP}:10873/caches/ \
    -rsync /www/logo rsync://${DST_IP}:10873/logo/ &
