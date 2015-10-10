import subprocess
import ldap
from stooge_ldap_mgmt import StoogeLDAPMgmt

MGR_CRED = 'cn=Manager,dc=unisonis,dc=com'
MGR_PASSWD = 'ldap4ec2'

class TestStoogeLDAPMgmt():

    def setup(self):
        # Load test LDAP entries from ldif file
        cmd = 'ldapadd -x -D "%s" -w %s -f test_stooges.ldif' % (MGR_CRED, MGR_PASSWD)
        subprocess.call(cmd,
                        shell=True,
                        stdout=open('/dev/null', 'w'),
                        stderr=subprocess.STDOUT)

    def teardown(self):
        # Delete test LDAP entries
        cmd = 'ldapdelete -x -D "%s" -w %s -c -f delete_test_stooges.ldif' % (MGR_CRED, MGR_PASSWD)
        subprocess.call(cmd,
                        shell=True,
                        stdout=open('/dev/null', 'w'),
                        stderr=subprocess.STDOUT)

    def test_list_stooges(self):
        l = StoogeLDAPMgmt()
        stooges_list = l.list_stooges(stooge_filter='o=teststooges', attrib=['cn', 'mail', 'homePhone'])
        assert stooges_list == ["cn: ['Test Larry Fine']", "mail: ['TestLFine@unisonis.com']", "homePhone: ['800-555-1313']", "cn: ['Test Moe Howard']", "mail: ['TestMHoward@unisonis.com']", "homePhone: ['800-555-1313']", "cn: ['Test Curley Howard']", "mail: ['TestCHoward@unisonis.com']", "homePhone: ['800-555-1313']"]

    def test_add_stooge(self):
        l = StoogeLDAPMgmt()

        # add new stooge: Harry Potter
        stooge_name = 'Test Harry Potter'
        stooge_ou = 'TestMemberGroupB'
        stooge_info = {'cn': ['Test Harry Potter'], 'objectClass': ['top', 'person', 'organizationalPerson', 'inetOrgPerson'], 'uid': ['harry'], 'title': ['QA Engineer'], 'facsimileTelephoneNumber': ['800-555-3318'], 'userPassword': ['harrysecret'], 'postalCode': ['75206'], 'mail': ['HPotter@unisonis.com'], 'postalAddress': ['2908 Greenville Ave.'], 'homePostalAddress': ['14 Cherry Ln. Plano TX 78888'], 'pager': ['800-555-1319'], 'homePhone': ['800-555-7777'], 'telephoneNumber': ['(800)555-1214'], 'givenName': ['Harry'], 'mobile': ['800-555-1318'], 'l': ['Dallas'], 'o': ['teststooges'], 'st': ['TX'], 'sn': ['Potter'], 'ou': ['TestMemberGroupB'], 'destinationIndicator': ['/bios/images/hpotter.jpg'], }

        l.add_stooge(stooge_name, stooge_ou, stooge_info)

        # verify the addition
        stooges_list = l.list_stooges(stooge_filter='o=teststooges', attrib=['cn', 'mail', 'homePhone'])
        assert stooges_list == ["cn: ['Test Larry Fine']", "mail: ['TestLFine@unisonis.com']", "homePhone: ['800-555-1313']", "cn: ['Test Moe Howard']", "mail: ['TestMHoward@unisonis.com']", "homePhone: ['800-555-1313']", "cn: ['Test Curley Howard']", "mail: ['TestCHoward@unisonis.com']", "homePhone: ['800-555-1313']", "cn: ['Test Harry Potter']", "mail: ['HPotter@unisonis.com']", "homePhone: ['800-555-7777']"]

    def test_modify_stooge(self):
        l = StoogeLDAPMgmt()

        # modify home phone for one of the stooges
        stooge_name = 'Test Larry Fine'
        stooge_ou = 'TestMemberGroupA'
        stooge_modified_attrib = [(ldap.MOD_REPLACE, 'homePhone', '800-555-8888')]
        l.modify_stooge(stooge_name, stooge_ou, stooge_modified_attrib)

        # verify the modification
        stooges_list = l.list_stooges(stooge_filter='o=teststooges', attrib=['cn', 'mail', 'homePhone'])
        assert stooges_list == ["cn: ['Test Larry Fine']", "mail: ['TestLFine@unisonis.com']", "homePhone: ['800-555-8888']", "cn: ['Test Moe Howard']", "mail: ['TestMHoward@unisonis.com']", "homePhone: ['800-555-1313']", "cn: ['Test Curley Howard']", "mail: ['TestCHoward@unisonis.com']", "homePhone: ['800-555-1313']"]


    def test_delete_stooge(self):
        l = StoogeLDAPMgmt()

        # delete one of the stooges
        stooge_name = 'Test Curley Howard'
        stooge_ou = 'TestMemberGroupB'

        l.delete_stooge(stooge_name, stooge_ou)

        # verify the deletion
        stooges_list = l.list_stooges(stooge_filter='o=teststooges', attrib=['cn', 'mail', 'homePhone'])
        assert stooges_list == ["cn: ['Test Larry Fine']", "mail: ['TestLFine@unisonis.com']", "homePhone: ['800-555-1313']", "cn: ['Test Moe Howard']", "mail: ['TestMHoward@unisonis.com']", "homePhone: ['800-555-1313']"]
