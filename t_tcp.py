#!/usr/bin/env python

import gevent.monkey
gevent.monkey.patch_all()
from gevent import socket
from gevent.server import StreamServer

SERVE_PORT = 8080


def log(*args):
    print args


def hi_back(sock, address):
    fp = sock.makefile()
    fp.read(1)
    fp.write('h')
    fp.flush()
    sock.shutdown(socket.SHUT_WR)
    sock.close()


def serve_http(ip):
    log('start serve_http %s:%s...' % (ip, SERVE_PORT))
    server = StreamServer((ip, SERVE_PORT), hi_back, spawn=16)
    server.serve_forever()


def say_hi(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, SERVE_PORT))
    sock.send("h")
    return sock.recv(64)


if __name__ == "__main__":
    import sys
    is_client = False
    if len(sys.argv) > 1:
        is_client = sys.argv[1] == 'c'
    ip = '127.0.0.1'
    if is_client:
        print say_hi(ip)
    else:
        serve_http(ip)
