#!/bin/env python

#ldapadd -x -D "cn=kingsoft,dc=myksc,dc=com" -W -f stooges.ldif
#ldapsearch -x -b 'dc=myksc,dc=com' '(o=stooges)'


import ldap

LDAP_HOST = '123.59.14.251'
LDAP_BASE_DN = 'DC=myksc,DC=com'
MGR_CRED = 'CN=kingsoft,CN=Users,DC=myksc,DC=com'
MGR_PASSWD = 'Ksc123456'
#add oganization unit first
STOOGE_OU = 'MemberGroupB'
STOOGE_FILTER = 'o=stooges'

class StoogeLDAPMgmt:

    def __init__(self, ldap_host=None, ldap_base_dn=None, mgr_cred=None, mgr_passwd=None):
        if not ldap_host:
            ldap_host = LDAP_HOST
        if not ldap_base_dn:
            ldap_base_dn = LDAP_BASE_DN
        if not mgr_cred:
            mgr_cred = MGR_CRED
        if not mgr_passwd:
            mgr_passwd = MGR_PASSWD
        self.ldapconn = ldap.open(ldap_host)
        self.ldapconn.simple_bind(mgr_cred, mgr_passwd)
        self.ldap_base_dn = ldap_base_dn

    def list_stooges(self, stooge_filter=None, attrib=None):
        if not stooge_filter:
            stooge_filter = STOOGE_FILTER

        import pdb; pdb.set_trace()  # at xxx.py:line_number
        s = self.ldapconn.search_s(self.ldap_base_dn, ldap.SCOPE_SUBTREE, stooge_filter, attrib)
        print "Here is the complete list of stooges:"
        stooge_list = []
        for stooge in s:
            attrib_dict = stooge[1]
            for a in attrib:
                out = "%s: %s" % (a, attrib_dict[a])
                print out
                stooge_list.append(out)
        return stooge_list

    def add_stooge(self, stooge_name, stooge_ou, stooge_info):
        stooge_dn = 'cn=%s,ou=%s,%s' % (stooge_name, stooge_ou, self.ldap_base_dn)
        stooge_attrib = [(k, v) for (k, v) in stooge_info.items()]
        print "Adding stooge %s with ou=%s" % (stooge_name, stooge_ou)
        self.ldapconn.add_s(stooge_dn, stooge_attrib)

    def modify_stooge(self, stooge_name, stooge_ou, stooge_attrib):
        stooge_dn = 'cn=%s,ou=%s,%s' % (stooge_name, stooge_ou, self.ldap_base_dn)
        print "Modifying stooge %s with ou=%s" % (stooge_name, stooge_ou)
        self.ldapconn.modify_s(stooge_dn, stooge_attrib)

    def delete_stooge(self, stooge_name, stooge_ou):
        stooge_dn = 'cn=%s,ou=%s,%s' % (stooge_name, stooge_ou, self.ldap_base_dn)
        print "Deleting stooge %s with ou=%s" % (stooge_name, stooge_ou)
        self.ldapconn.delete_s(stooge_dn)

if __name__ == "__main__":
        l = StoogeLDAPMgmt()
        raw_input('readly...\n')

        # add new stooge: Harry Potter
        stooge_name = 'Harry Potter'
        stooge_ou = STOOGE_OU
        stooge_info = {'cn': ['Harry Potter'], 'objectClass': ['top', 'person', 'organizationalPerson', 'inetOrgPerson'],
                       'uid': ['harry'], 'title': ['QA Engineer'], 'facsimileTelephoneNumber': ['800-555-3318'],
                       'userPassword': ['harrysecret'], 'postalCode': ['75206'], 'mail': ['HPotter@myksc.com'],
                       'postalAddress': ['2908 Greenville Ave.'], 'homePostalAddress': ['14 Cherry Ln. Plano TX 78888'],
                       'pager': ['800-555-1319'], 'homePhone': ['800-555-7777'], 'telephoneNumber': ['(800)555-1214'],
                       'givenName': ['Harry'], 'mobile': ['800-555-1318'], 'l': ['Dallas'], 'o': ['stooges'],
                       'st': ['TX'], 'sn': ['Potter'], 'ou': [stooge_ou], 'destinationIndicator': ['/bios/images/hpotter.jpg'], }

        l.add_stooge(stooge_name, stooge_ou, stooge_info)
        l.set_option(ldap.OPT_REFERRALS, 0)
        # see if it was added
        l.list_stooges(attrib=['cn', 'mail', 'homePhone'])

        # now modify home phone
        stooge_modified_attrib = [(ldap.MOD_REPLACE, 'homePhone', '800-555-8888')]
        try:
            l.modify_stooge(stooge_name, stooge_ou, stooge_modified_attrib)
        except ldap.LDAPError, error:
            print 'problem with ldap',error


        # now delete Harry Potter
        l.delete_stooge(stooge_name, stooge_ou)

        # see if it was deleted
        l.list_stooges(attrib=['cn', 'mail', 'homePhone'])
