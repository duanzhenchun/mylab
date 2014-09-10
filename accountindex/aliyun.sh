yum -y install readline-devel mysql mysql-devel gcc pcre pcre-devel zlib zlib-devel openssl openssl-devel gcc-c++ autoconf automake glibc-devel 

#vim /etc/ld.so.conf #新增
#/usr/local/lib
#/usr/local/lib64
ldconfig

wget http://python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2
tar -jxvf Python-2.7.3.tar.bz2 
cd Python-2.7.3
./configure
make && make install
cd ..

# verify
python -V

#pip
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py --no-check-certificate
sudo python get-pip.py

pip install django MySQL-python 

#mysql -u leo -p -h 118.25.206.182 -P 3307 WeiboPanel<access_token.sql
