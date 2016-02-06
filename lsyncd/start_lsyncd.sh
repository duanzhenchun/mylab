#!/bin/bash

if [ $# -ne 1 ]; then
  echo "usage: start_lsyncd.sh MOUNT_POINT"
  exit 1
fi


DIR=`(cd \`dirname $0\`; pwd -P)`

source ./env_lsync.sh

mkdir -p $DIR/ssh
cp ${DIR}/ssh_config $DIR/ssh/config

cp $LsyncdIdentityFile $DIR/ssh
chown root:root ${DIR}/ssh/id_rsa

docker run -d -p 2202 --name kfile_lsyncd \
    --net host \
    -v $DIR/ssh:/root/.ssh:rw \
    -v $1:/mnt/data \
    -e TARGET_DIR=${TARGET_DIR} \
    123.59.14.139:5000/kingfile/lsyncd
