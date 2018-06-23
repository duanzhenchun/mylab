#!/usr/bin/env python
# encoding: utf-8

from IpSearch import IpSearch

finder = IpSearch("ip-3.0.dat", debug=False)


def show(ip):
    result = finder.lookup(ip)
    print('%s: %s' %(ip, result))


ip_list = ['1.1.1.1', '8.8.8.8', '114.114.114.114']
for index, ip in enumerate(ip_list):
    show(ip)

# |Cloudflare||||CloudflareDNS/APNIC|||||
# 北美洲|美国||||GoogleDNS||United States|US|-95.712891|37.09024
# 亚洲|中国|江苏|南京|秦淮|114DNS|320104|China|CN|118.79815|32.01112
while True:
    ip4 = raw_input('input ip4(or q):')
    if 'q' == ip4:
        break
    else:
        show(ip4)
