#!/usr/bin/env python
# encoding: utf-8


import gevent
from gevent import socket
#import gevent.dns;
from gevent import monkey
monkey.patch_socket()

import redis
from dnslib import DNSHeader, DNSRecord, QTYPE, RR,A, MX


A_RECORD_PREFIX = 'DNS:PASSTHRU:A:%s'
TXT_RECORD_PREFIX = 'DNS:PASSTHRU:TXT:%s'
CNAME_RECORD_PREFIX = 'DNS:PASSTHRU:CNAME:%s'

AF_INET = 2
SOCK_DGRAM = 2

s = socket.socket(AF_INET, SOCK_DGRAM)
s.bind(('', 9053))


def dns_handler(s, peer, data, r):
    request = DNSRecord.parse(data)
    id = request.header.id
    qname = request.q.qname
    qtype = request.q.qtype

    IP = r.get(A_RECORD_PREFIX % qname)
    TXT = r.get(TXT_RECORD_PREFIX % qname)
    CNAME = r.get(CNAME_RECORD_PREFIX % qname)

    if not IP:
        try:
            IP = socket.gethostbyname(str(qname))
        except Exception, e:
            print e
            print 'Host not found'
            IP = '0.0.0.0'

    print "Request (%s): %r (%s) - Response: %s" % (str(peer), qname.label,
                                                       QTYPE[qtype], IP)

    reply = DNSRecord(DNSHeader(id=id, qr=1, aa=1, ra=1), q=request.q)

    if qtype == QTYPE.A:
        reply.add_answer(RR(qname, qtype, rdata=A(IP)))
    elif qtype == QTYPE['*']:
        reply.add_answer(RR(qname, QTYPE.A, rdata=A(IP)))
        reply.add_answer(RR(qname, QTYPE.MX, rdata=MX(IP)))
        reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(TXT)))
    else:
        reply.add_answer(RR(qname, QTYPE.CNAME, rdata=CNAME(TXT)))
    s.sendto(reply.pack(), peer)


def main():
    r = redis.Redis()
    while True:
        data, peer = s.recvfrom(8192)
        gevent.spawn(dns_handler, s, peer, data, r)

if __name__ == '__main__':
    main()
