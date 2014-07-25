#now=$(date +"%Y_%m%d_%H%M")
#mysqldump -h localhost -uroot -p onion>data/onion_$now.sql
#redis-cli bgsave 
#sudo cp /var/lib/redis/dump.rdb data/

#for i in 54.250.166.126 
for i in 182.92.99.134
do
    rsync -avz --cvs-exclude '.git/ *~ .pyc .swp' "-e ssh" ../onion root@$i:src/ 
done

#aws prepare
#import nltk; nltk.download(); d wordnet;q
#set nginx.conf for static, like /tmp/static

#db backup
#http://redis4you.com/articles.php?id=010
#crontab -e
#@weekly redis-cli bgsave
#@weekly mysqldump -h localhost -uroot -p12345 onion>data/onion.sql
