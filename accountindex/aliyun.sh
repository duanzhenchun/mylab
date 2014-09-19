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

#mysql -u leo -p -h 118.25.206.182 -P 3307 WeiboPanel<access_token.sql
#cd src/crawl/ && nohup python crawl_relation.py ../../data/filter_uniq_2.txt > out_2.txt &

crontab -e
0 */4 * * * sh /root/src/accountindex/stats.sh
