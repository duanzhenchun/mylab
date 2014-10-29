yum -y install readline-devel mysql mysql-devel gcc pcre pcre-devel zlib zlib-devel openssl openssl-devel gcc-c++ autoconf automake glibc-devel 

#vim /etc/ld.so.conf #新增
#/usr/local/lib
#/usr/local/lib64
ldconfig

cd ~/
wget http://python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2
tar -jxvf Python-2.7.3.tar.bz2 
cd Python-2.7.3
./configure
make && make install
cd ..

# modify for yum
mv /usr/bin/python /usr/bin/python.bak
ln -s /usr/local/bin/python2.7 /usr/bin/python
sed -ie 's#/usr/bin/python$#/usr/bin/python2.6#g' /usr/bin/yum

# verify
python -V

#pip
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py --no-check-certificate
python get-pip.py

pip install django MySQL-python 


:<<COMMENT
#prepare mysql db disk
fdisk /dev/xvdb
    n, p, 1, ret, ret, wq
mkfs.ext3 /dev/xvdb1
echo '/dev/xvdb1 /mnt ext3 defaults 0 0' >> /etc/fstab
mount -a
df -h

vim /etc/my.cnf
    [mysqld]
    datadir=/mnt/mysql
/etc/init.d/mysqld start
mysqladmin -u root password cicdata

mysql -pcicata -e "create database WeiboPanel"
mysql -pcicdata WeiboPanel<data/WeiboPanel_tbl.sql
mysql -pcicdata WeiboPanel<data/access_token.sql

#divide table
for i in $(seq 0 9);do 
    for table in Weibo_User_Profile Weibo_User_Relationship;do
	#echo "${table}_$i"
    mysql -pcicdata WeiboPanel -e "create table ${table}_$i like ${table}"
    done
done
mysql -pcicdata WeiboPanel -e "show tables"

#cicstore
    mysql -u leo -p -h 118.25.206.182 -P 3307 

#crawl
cd src/crawl/ && nohup python crawl_relation.py ../../data/xaa> out.txt &

#stats
crontab -e
    0 */4 * * * sh /root/src/accountindex/stats.sh

COMMENT
