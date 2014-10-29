for i in 182.92.235.144 182.92.69.210 182.92.169.80 
do
    rsync -avz --cvs-exclude '*~ .pyc .swp' "-e ssh" ../accountindex root@$i:src/ 
done

:<<COMMENT
#aws prepare
import nltk; nltk.download(); d wordnet;q
#set nginx.conf for static, like /tmp/static

#db backup
#http://redis4you.com/articles.php?id=010
crontab -e
    @weekly redis-cli bgsave
    @weekly mysqldump -h lo

ssh root@182.92.69.210
ssh root@182.92.169.80
ssh root@182.92.218.82  #db

COMMENT
