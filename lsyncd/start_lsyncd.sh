#!/bin/bash

# ssh-keygen -t rsa -C 'root@231' -N "" -f ~/.ssh/id_rsa

DIR=`(cd \`dirname $0\`; pwd -P)`

CONTAINER_PREFIX="kfile_"
CONTAINER_DATA_NAME=${CONTAINER_PREFIX}"data"

source ./env_lsync.sh

if [ ! -d ${DIR}/ssh ]; then
    mkdir -p $DIR/ssh
    cp ${DIR}/ssh_config $DIR/ssh/config
    sed -i "s/HostName.*/HostName ${PEER_IP}/" $DIR/ssh/config
    cp $LsyncdIdentityFile $DIR/ssh
    ssh-keyscan ${PEER_IP} >> $DIR/ssh/known_hosts
fi

chown -R root:root ${DIR}/ssh

docker run -d -p 22 --name kfile_lsyncd \
    --net host \
    --volumes-from ${CONTAINER_DATA_NAME} \
    -v $DIR/ssh:/root/.ssh:rw \
    -v SYNC_DIR:/sync_dir \
    -e SYNC_DIR=${SYNC_DIR} \
    kfile.registry.com:5001/kingfile/lsyncd
