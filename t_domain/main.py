#!/usr/bin/env python
# encoding: utf-8

# requirement
# sudo yum install python-gevent
# python2.6+

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
HTTP_TIMEOUT = 3
PROBE_TIMEOUT = 10
SERVER_NAME = "kcache.hc.org"
FILE_2M = "2M.dat"
# TODO random str
TEST_UP_PORT = 8081
SERVE_PORT = 8089
DOMAIN_CONF = './domain.conf'
AUTH_CONF = './auth_domain.conf'
ANYHOST = "./anyhost"

FAKE_IPS = ['103.192.253.225', '222.222.207.9', '123.123.123.123']

domain_conf_title = "#Host Info Detect Times WarnTime(S) good_time(s) Len(Byte) Good_Ip Modify Backup Method Code Ip" [
    1:].split()
COL_IP = domain_conf_title.index('Ip')
COL_BACKUP = domain_conf_title.index('Backup')
COL_GOOD_IP = domain_conf_title.index('Good_Ip')

if ONLINE:
    squid_path = "/usr/local/squid/etc/"
    DOMAIN_CONF = squid_path + DOMAIN_CONF
    AUTH_CONF = squid_path + AUTH_CONF

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
"""


def parse_auth_conf():
    dic = {}
    with open(AUTH_CONF) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            domain, url, ips = line.split()
            # TODO probe together
            sorted_ips = probe(ips.split('|'), url)
            dic[domain] = (url, sorted_ips)
    return dic


def parse_conf():
    all_ip = set()
    domain_needs = {}
    domain_auth = {}
    auth_dic = parse_auth_conf()
    print "auth_dic:", auth_dic

    for line in open(DOMAIN_CONF):
        line = line.strip()
        if not line:
            continue
        for neg in NEGLECT:
            if line.startswith(neg):
                break
        else:
            # valid line
            col = line.split()
            domain = col[0]
            num_need = int(col[COL_GOOD_IP])
            ips = col[COL_IP].split('|')
            if WILD == domain:
                wild_ips = ips[:num_need]  # do not need to probe
            elif domain in auth_dic:
                domain_auth[domain] = auth_dic[domain][1][:num_need]
            else:
                ips = set(ips)
                backups = col[COL_BACKUP]
                if "no" != backups:
                    backups = backups.split('|')
                    all_ip.update(set(backups))
                else:
                    backups = None
                domain_needs[domain] = (num_need, backups, ips)
                all_ip.update(ips)

    up_ips = []
    for ip in all_ip:
        if valid_ip4(ip):
            up_ips.append(ip)
    assert valid_ips_num[0] < len(up_ips) < valid_ips_num[1]
    print "wild_ips:", wild_ips
    print "len(up_ips):", len(up_ips)
    print "len(domain_needs):", len(domain_needs)
    return up_ips, wild_ips, domain_needs, domain_auth


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


def filter_needs(sorted_ips, ips, num_need):
    res = []
    for ip in sorted_ips:
        if ip in ips:
            res.append(ip)
            if len(res) >= num_need:
                break
    return res


def write_anyhost(sorted_ips, wild_ips, domain_needs, domain_auth):
    with open(ANYHOST, 'w') as fo:
        fo.write(ANYHOST_HEADER)
        for ip in wild_ips:
            write_host_format(fo, WILD, ip)
        for domain, ips in domain_auth.iteritems():
            for ip in ips:
                write_host_format(fo, domain, ip)
        for domain, (num_need, backups, ips) in domain_needs.iteritems():
            filtered = filter_needs(sorted_ips, ips, num_need)
            if filtered:
                print ips, sorted_ips
                for ip in filtered:
                    write_host_format(fo, domain, ip)
            elif backups:
                filtered = filter_needs(sorted_ips, backups, num_need)
                for ip in filtered:
                    write_host_format(fo, domain, ip)
            # TODO if none available, set all or all backup


def write_host_format(fo, domain, ip):
    #  bigota.d.miui.com.       IN      A       183.131.29.65 ; 0.092871 ip ip_work 404 Y
    fo.write("%s\tIN\tA\t%s\n" % (domain, ip))


def alert(trace):
    print trace
    #mail.send(trace)


def loop_probe():
    while True:
        start = time.time()
        try:
            res = parse_conf()
            sorted_ips = probe(res[0])
            write_anyhost(sorted_ips, *res[1:])
        except:
            alert(traceback.print_exc())
        to_rest = PERIOD - int(time.time() - start)
        assert to_rest > 0, "to_rest: %d" %to_rest
        print 'sleep:', to_rest
        gevent.sleep(to_rest)


def probe(ips, url=None):
    if not ONLINE and None == url:
        ips = FAKE_IPS
    print 'start probe ips:', ips
    jobs = [gevent.spawn(http_time, ip, url) for ip in ips]
    gevent.joinall(jobs, timeout=PROBE_TIMEOUT)
    res = sorted([job.value or (None, None) for job in jobs])
    print 'res to be sorted:', res
    sorted_ips = []
    for i in res:
        if i:
            t, ip = i
            if t:
                sorted_ips.append(ip)
    return sorted_ips


def serve_file(environ, start_response):
    with open(ANYHOST, 'r') as fp:
        start_response('200 OK', [('Content-Type', 'text/html')])
        #  yield f.read()
        while True:
            chunk = fp.read(4096)
            if not chunk: break
            yield chunk


def serve_http():
    print 'start serve_http...'
    server = pywsgi.WSGIServer(('', SERVE_PORT), serve_file)
    server.serve_forever()


def http_time(ip, url):
    if url:
        host_name, path = url.split('/', 1)
    else:
        host_name, path = SERVER_NAME, FILE_2M
    headers = {"Host": host_name}
    port_str = ""
    if not ONLINE and not url:
        port_str = ":%d" %TEST_UP_PORT
    s = "http://%s%s/%s" % (ip, port_str, path)
    print 'url str:', s, 'host_name:', host_name
    req = urllib2.Request(s, headers=headers)
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
    gevent.joinall([gevent.spawn(loop_probe),
                    gevent.spawn(serve_http)])
