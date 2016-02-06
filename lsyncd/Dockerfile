FROM 123.59.14.139:5000/kingfile/board

ENV USER lsyncd
ENV PASSWORD lsyncd

# Install lsyncd
RUN apt-get install -y lsyncd

# already Install ssh
#RUN apt-get install -y openssh-server sudo && mkdir /var/run/sshd

# Add user
RUN useradd $USER && adduser $USER sudo && echo "${USER}:${PASSWORD}" |chpasswd && mkdir /home/$USER && chown -R $USER /home/$USER && chsh -s /bin/bash $USER

# mkdir for mouting data directory
RUN mkdir -p /mnt/data

EXPOSE 2202

CMD sed -i 's/#   Port 22/Port 2202/' /etc/ssh/ssh_config && \
     /usr/sbin/sshd -p 2202 -D
# lsyncd -nodaemon -rsyncssh /mnt/data lsyncd_target ${TARGET_DIR}
