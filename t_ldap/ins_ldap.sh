yum install openldap-* -y

#拷贝LDAP配置文件到LDAP目录
cp /usr/share/openldap-servers/slapd.conf.obsolete /etc/openldap/slapd.conf

# slappasswd
#输入完密码后,返回一串密文，先保存到剪贴板
#{SSHA}pfAJm+JJa4ec2y8GjTc8uMEJpoR5YKLy

vi /etc/openldap/slapd.conf
#Add entries:
database bdb
suffix "dc=myksc,dc=com"
rootdn "cn=kingsoft,dc=myksc,dc=com"
rootpw {SSHA}pasted_from_slappasswd_output
directory /var/lib/ldap

rm -rf /etc/openldap/slapd.d/*
cp /usr/share/openldap-servers/DB_CONFIG.example  /var/lib/ldap/DB_CONFIG

chown -R ldap:ldap /var/lib/ldap
chown -R ldap:ldap /etc/openldap/
chown -R ldap:ldap /etc/openldap/slapd.d

service slapd restart
chkconfig slapd on

#test
slaptest  -f /etc/openldap/slapd.conf -F /etc/openldap/slapd.d
ldapsearch -x -b '' -s base '(objectclass=*)' namingContexts

#使用 ldapadd 和 LDIF 文件在 LDAP 数据库中添加更多条目
ldapadd -x -D "cn=kingsoft,dc=myksc,dc=com" -W -f myksc.ldif
ldapadd -x -D "cn=kingsoft,dc=myksc,dc=com" -W -f stooges.ldif
ldapsearch -x -b 'dc=myksc,dc=com' '(o=stooges)'


#remote win
CMD_PRE="ldapsearch -x -LLL -D cn=kingsoft,cn=Users,dc=myksc,dc=com -h 123.59.14.251 -w Ksc123456"
#${CMD_PRE} -b ou=ceshi,dc=myksc,dc=com -s one dn
#${CMD_PRE} -b ou=ceshi,dc=myksc,dc=com -s sub dn
#${CMD_PRE} -b ou=ceshi,dc=myksc,dc=com -s sub '(objectClass=organizationalUnit)' dn
${CMD_PRE} -b ou=ceshi2,ou=ceshi,dc=myksc,dc=com -s one'(objectClass=person)' dn
