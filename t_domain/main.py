#!/usr/bin/env python
# encoding: utf-8

import gevent
import gevent.monkey
gevent.monkey.patch_all()
from gevent import pywsgi

import socket
import re
import time
import urllib2
import signal
import traceback

### configure
ONLINE = False

PERIOD = 60  #sec
HTTP_TIMEOUT = 5
PROBE_TIMEOUT = HTTP_TIMEOUT + 5
FILE_2M = "2M.dat"
UP_PORT = 8081
SERVE_PORT = 8089
DOMAIN_CONF = './domain.conf'
ORIGIN_IP_CONF = './origin_domain_ip'
ANYHOST = "./anyhost"

SERVER_NAME = "fake.com"
FAKE_IPS = ['103.192.253.225', '222.222.207.9', '123.123.123.123']

domain_conf_title = "#Host Info Detect Times WarnTime(S) good_time(s) Len(Byte) Good_Ip Modify Backup Method Code Ip"[1:].split()
COL_GOOD_IP = domain_conf_title.index('Good_Ip')
COL_IP = domain_conf_title.index('Ip')
COL_BACKUP = domain_conf_title.index('Backup')

if ONLINE:
    SERVER_NAME = "kcache.hc.org"
    squid_path = "/usr/local/squid/etc/"
    DOMAIN_CONF = squid_path + DOMAIN_CONF
    ORIGIN_IP_CONF = squid_path + ORIGIN_IP_CONF

WILD = 'wild.'
NEGLECT = ('#', '*')
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
            with open(ORIGIN_IP_CONF) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    d, ips = line[0], line[1].split(':')
                    _dic[d] = ips
            _dic["done"] = True

    return _get(domain)


def parse_conf():
    all_ip = set()
    domain_needs={}
    domain_origin={}

    for line in open(DOMAIN_CONF):
        line = line.strip()
        if not line:
            continue
        if line.startswith(WILD):
            col = line.split()
            wild_ips = col[COL_IP][:COL_GOOD_IP] # do not need to probe
            continue
        for neg in NEGLECT:
            if line.startswith(neg):
                break
        else:
            # valid line
            col = line.split()
            domain = col[0]
            if len(col) > EXTRA_COL:
                domain_origin[domain] = get_origin_ips(domain)
            else:
                ips = set(col[COL_IP].split('|'))
                domain_needs[domain] = (col[COL_GOOD_IP], col[COL_BACKUP], ips)
                all_ip.update(ips)

    up_ips = []
    for ip in all_ip:
        if valid_ip4(ip):
            up_ips.append(ip)
    assert valid_ips_num[0] < len(up_ips) < valid_ips_num[1]
    print "up_ips:", up_ips, "wild_ips:", wild_ips, "len(domain_needs):", len(domain_needs), 'len(domain_origin):', len(domain_origin)
    return up_ips, wild_ips, domain_needs, domain_origin


def valid_ip4(addr):
    return re.match(ip4_pattern, addr)


def benchmark(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print '%s %f %s' % (f.__name__, time.time() - t, 'sec')
        return res

    return wrapper


# to smooth up bandwidth
def hash_wait():
    hn = socket.gethostname()
    sec = hash(hn) % PERIOD
    print 'hash wait %s sec' % sec
    if ONLINE:
        time.sleep(sec)


def output_anyhost(sorted_ips, wild_ips, domain_needs, domain_origin):
    with open(ANYHOST, 'w') as fo:
        fo.write(ANYHOST_HEADER)
        for ip in wild_ips:
            write_host_format(fo, WILD, ip)
        for domain, ips in domain_origin.iteritems():
            for ip in ips:
                write_host_format(fo, domain, ip)
        for domain, (num, backup, ips) in domain_needs.iteritems():
            filtered = []
            for ip in sorted_ips:
                if ip in ips:
                    filtered.append(ip)
                    if len(filtered) > num:
                        break
            if filtered:
                for ip in filtered:
                    write_host_format(fo, domain, ip)
            elif 'no' != backup:
                write_host_format(fo, domain, backup)


def valid_domain():
    pass


def write_host_format(fo, domain, ip):
    #  bigota.d.miui.com.       IN      A       183.131.29.65 ; 0.092871 ip ip_work 404 Y
    fo.write("%s\tIN\tA\T%s;\n" % (domain, ip))


def alert(trace):
    print trace
    #mail.send(trace)

def loop_probe():
    while True:
        try:
            res = parse_conf()
            sorted_ips = probe(res[0])
            output_anyhost(sorted_ips, *res[1:])
        except:
            alert(traceback.print_exc())
        gevent.sleep(PERIOD)


def probe(ips):
    if not ONLINE:
        ips = FAKE_IPS
    print 'start probe ips:', ips
    jobs = [gevent.spawn(http_time, ip) for ip in ips]
    gevent.joinall(jobs, timeout=PROBE_TIMEOUT)
    res = sorted([job.value for job in jobs])
    print 'sorted:', res
    sorted_ips = []
    for (t, ip) in res:
        if t:
            sorted_ips.append(ip)
    return sorted_ips


def serve_file(environ, start_response):
    f = open(ANYHOST, 'r')
    start_response('200 OK', [('Content-Type', 'text/html')])
    yield f.read()


def serve_result():
    print 'start serve_result...'
    server = pywsgi.WSGIServer(('', SERVE_PORT), serve_file)
    server.serve_forever()


def http_time(ip):
    headers = {"Host": SERVER_NAME}
    req = urllib2.Request("http://%s:%d/%s" % (ip, UP_PORT, FILE_2M),
                          headers=headers)
    start = time.time()
    t = None
    try:
        resp = urllib2.urlopen(req, timeout=HTTP_TIMEOUT)
        resp.read()
        t = time.time() - start
    except:  #  any exception: urllib2.URLError, socket.error, etc
        pass
    return (t, ip)


if __name__ == "__main__":
    hash_wait()
    gevent.signal(signal.SIGQUIT, gevent.kill)
    gevent.joinall([gevent.Greenlet.spawn(loop_probe), gevent.spawn(
        serve_result)])
