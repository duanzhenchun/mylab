from pysnmp.hlapi import *

commu = 'public'
host = '192.168.0.1'

oids = ['1.3.6.1.2.1.31.1.1.1.6', '1.3.6.1.2.1.31.1.1.1.10']


def walk(host, target):
    for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
            SnmpEngine(),
            CommunityData(commu),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity('IF-MIB',target)),
            lexicographicMode=False):
        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print(
                '%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break
        else:
            for varBind in varBinds:
                print(varBind)

for target in ('ifHCInOctets', 'ifHCOutOctets'):
    walk(host, target)
