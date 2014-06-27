#now=$(date +"%Y_%m%d_%H%M")
#mysqldump -h localhost -uroot -p onion>data/onion_$now.sql
#redis-cli bgsave cp /var/lib/dump.rdb data/

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
#DEBUG = False
#ln -s $HOME/env/lib/python2.7/site-packages/django/contrib/admin static/
#python manage.py collectstatic
# uwsgi --reload uwsgi.pid 

#db backup
#http://redis4you.com/articles.php?id=010
#crontab -e
#@weekly redis-cli bgsave
#@weekly mysqldump -h localhost -uroot -p12345 onion>/home/whille/bak/onion.sql
