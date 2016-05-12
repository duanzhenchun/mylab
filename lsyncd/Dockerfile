FROM kfile.registry.com:5001/kingfile/board

ENV USER lsyncd
ENV PASSWORD lsyncd

# Install lsyncd
RUN apt-get install -y lsyncd

# already Install ssh
#RUN apt-get install -y openssh-server sudo && mkdir -p /var/run/sshd

# Add user
RUN useradd $USER && adduser $USER sudo && echo "${USER}:${PASSWORD}" |chpasswd && mkdir /home/$USER && chown -R $USER /home/$USER && chsh -s /bin/bash $USER

EXPOSE 22

# multiple -rsyncssh is available
CMD ln -s /caches   /sync_dir/ && \
    ln -s /www/logo /sync_dir/ && \
    lsyncd -nodaemon -delay 5 \
        -rsyncssh /sync_dir lsyncd_target ${SYNC_DIR}
