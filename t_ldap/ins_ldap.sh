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

ADM_DN="cn=kingsoft,${DC}"
# set passwd here
ADM_PWD=

DC="dc=myksc,dc=com"
#linux
HOST="192.168.138.131"
#windows
# HOST="123.59.14.251"
# ADM_DN="cn=kingsoft,cn=Users,${DC}"

export LDAP_ARG="-x -w $ADM_PWD -D ${ADM_DN} -H ldap://${HOST}/389"

#add domain
#ldapadd ${LDAP_ARG} -f myksc.ldif

DEPT_NUM=5

#delete recursively
for d1 in $(seq $DEPT_NUM);do
    ldapdelete ${LDAP_ARG} "ou=dept${d1},dc=myksc,dc=com" -r
done

#add depts and person
sh ./add_depts.sh $DEPT_NUM

#search examples
ldapsearch -x -b 'dc=myksc,dc=com' '(o=stooges)'
ldapsearch ${LDAP_ARG} -b ou=ceshi,dc=myksc,dc=com -s one dn
ldapsearch ${LDAP_ARG} -b ou=ceshi,dc=myksc,dc=com -s sub dn
ldapsearch ${LDAP_ARG} -b ou=ceshi,dc=myksc,dc=com -s sub '(objectClass=organizationalUnit)' dn
ldapsearch ${LDAP_ARG} -b ou=ceshi2,ou=ceshi,dc=myksc,dc=com -s one '(&(objectClass=person)(cn=person111))' dn
