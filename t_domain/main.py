#!/usr/bin/env python
# encoding: utf-8

import re
import time

ONLINE = False
DEBUG = True

TARGET_URL = "120.132.79.9:8001/static_file"
domain_conf = './domain.conf'
origin_ip_conf = './origin_domain_ip'
anyhost = "./anyhost"

domain_conf_title = "#Host Info Detect Times WarnTime(S) good_time(s) Len(Byte) Good_Ip Modify Backup Method Code  Ip"
COL_GOOD_IP = domain_conf_title.index('Good_Ip')
COL_IP = domain_conf_title.index('Ip')

if ONLINE:
    TARGET_URL = "kcache.hc.org/XXX"
    squid_path = "/usr/local/squid/etc/"
    domain_conf = squid_path + domain_conf
    origin_ip_conf = squid_path + origin_ip_conf
    anyhost = "/var/named/" + anyhost

PERIOD = 60  #sec
WILD = 'wild.'
neglect = ('#', '*')
EXTRA_COL = 15
ip4_pattern = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
valid_ips_num = (1, 10000)

ANYHOST_HEADER = """;-----
$TTL 60
$ORIGIN .
@ IN SOA ns1. root.localhost. (
        1480421762;
        7000;
        3000;
        15000;
        86400;
);

@  86400         IN NS   ns1
ns1 86400       IN A    127.0.0.1

;-----
*.                       IN      CNAME   wild
*.cn.                    IN      CNAME   wild
*.com.                   IN      CNAME   wild
*.com.cn.                IN      CNAME   wild
*.gov.                   IN      CNAME   wild
*.gov.cn.                IN      CNAME   wild
*.edu.                   IN      CNAME   wild
*.edu.cn.                IN      CNAME   wild
wild.                    IN      A       218.61.35.185 ; inf ip ip_down 000 Y
"""


def get_origin_ips(domain):
    _dic = {}

    def _get(domain):
        if _dic:
            return _dic.get(domain, [])
        else:
            with open(origin_ip_conf) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    d, ips = line[0], line[1].split(':')
                    _dic[d] = ips
            _dic["done"] = True

    return _get(domain)


def get_upper_ips():
    all_ip = set()
    for line in open(domain_conf):
        line = line.strip()
        if not line:
            continue
        if line.startswith(WILD):
            wild_ip = line.split()[COL_IP]
            continue
        for neg in neglect:
            if line.startswith(neg):
                break
        else:
            # valid line
            col = line.split()
            if len(col) > EXTRA_COL:
                domain = col[0]
                ips = get_origin_ips(domain)
            else:
                ips = col[COL_IP].split('|')
            all_ip.update(ips)

    assert valid_ip4(wild_ip)
    up_ips = []
    for ip in all_ip:
        if valid_ip4(ip):
            up_ips.append(ip)
    assert valid_ips_num[0] < len(up_ips) < valid_ips_num[1]
    return up_ips, wild_ip


def valid_ip4(addr):
    return re.match(ip4_pattern, addr)


def benchmark(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print '%s %f %s' % (f.__name__, time.time() - t, 'sec')
        return res

    return wrapper

def hash_wait():
    import socket
    hn = socket.gethostname()
    sec = hash(hn)% PERIOD
    print 'wait %s sec' %sec
    time.sleep(sec)


def main():
    try:
        up_ips, wild_ip = get_upper_ips()
        if DEBUG:
            print "up_ips:", up_ips
            print "wild_ip:", wild_ip
        sort_ips = probe(up_ips)
        output_anyhost(sort_ips, wild_ip)
    except Exception, e:
        alert(e)


def probe(ips):
    return []


def output_anyhost(sort_ips, wild_ip):
    with open(anyhost, 'w') as fo:
        fo.write(ANYHOST_HEADER)
        fo.write(host_format(WILD, wild_ip))
        for domain, ips in valid_domain():
            for ip in filter(domain, ips):
                fo.write(host_format(domain, ip))


def valid_domain():
    pass


def host_format(domain, ip):
    #  bigota.d.miui.com.       IN      A       183.131.29.65 ; 0.092871 ip ip_work 404 Y
    return "%s\tIN\tA\T%s;\n" % (domain, ip)


def alert(e):
    #mail.send("alert")
    raise(e)

if __name__ == "__main__":
    main()
