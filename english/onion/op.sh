#now=$(date +"%Y_%m%d_%H%M")
#mysqldump -h localhost -uroot -p onion>data/onion_$now.sql
#dump db=1 redis to /var/lib/dump.rdb, cp to data/

for i in 54.250.166.126 
do
    rsync -avz --cvs-exclude '.git/ *~ .pyc .swp' "-e ssh" ../onion ec2-user@$i:src/ 
done

#aws prepare
#service stop redis
#sudo mv data/onion*.rdb /var/lib/redis/dump.rdb
#service start redis
#import nltk; nltk.download(); d wordnet;q
#set nginx.conf for static, like /tmp/static

#aws update
#setting.py:
#DEBUG = FALSE
#python manager.py collectstatic
