echo "$(date "+%Y-%m-%d %H:%M:%S")" `mysql -N -e  "select count(1) from Weibo_User_Relationship_1; select count(1) from Weibo_User_Profile_1"  -u root -pcicdata WeiboPanel` >>/root/src/stats.txt
