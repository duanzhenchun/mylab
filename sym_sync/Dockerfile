FROM debian:jessie
MAINTAINER whille whille@163.com

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends rsync lsyncd && \
  apt-get clean autoclean && \
  apt-get autoremove -y && \
  rm -rf /var/lib/apt/lists/*

EXPOSE 873
VOLUME /docker
ADD ./bin/run ./bin/start_lsync.sh /usr/local/bin/
ADD ./conf/rsyncd.conf /etc/

ENTRYPOINT ["/usr/local/bin/run"]
