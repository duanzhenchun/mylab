FROM 123.59.14.139:5000/kingfile/board

ENV USER lsyncd
ENV PASSWORD lsyncd

# Install lsyncd
RUN apt-get install -y lsyncd

# already Install ssh
#RUN apt-get install -y openssh-server sudo && mkdir -p /var/run/sshd

# Add user
RUN useradd $USER && adduser $USER sudo && echo "${USER}:${PASSWORD}" |chpasswd && mkdir /home/$USER && chown -R $USER /home/$USER && chsh -s /bin/bash $USER

# mkdir for mouting data directory
RUN mkdir -p /mnt/data

EXPOSE 22

CMD lsyncd -nodaemon -delay 5 -logfile /var/log/lsyncd.log -rsyncssh /mnt/data lsyncd_target ${TARGET_DIR}
