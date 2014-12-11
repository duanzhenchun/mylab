#start worker
for i in $(seq 4);do
    nohup python gearman_crawl.py -w >> worker_$i.log&
done

:<<COMMENT
#clear db table
for i in $(seq 0 9);do 
    mysql -N -e "drop table Weibo_tweet_$i; create table Weibo_tweet_$i like Weibo_tweet" -u root -pcicdata WeiboPanel
done

#start client
nohup python gearman_crawl.py -c /root/src/panel/out_10_7_1.txt>>cli.log&

#stop
ps ax|grep "python gearman_crawl.py"|grep -v grep|awk '{print $1}'|xargs kill

COMMENT
