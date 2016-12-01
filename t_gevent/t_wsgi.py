#!/usr/bin/env python
# encoding: utf-8

import gevent
import gevent.monkey
gevent.monkey.patch_all()

from gevent import pywsgi
import time
import urllib2
import signal

PERIOD = 10
HTTP_TIMEOUT = 5
PROBE_TIMEOUT = HTTP_TIMEOUT + 5
FAKE_HOST="fake.com"
UP_PORT = 8081

# to smooth up bandwidth
def hash_wait():
    print 'hash_wait'
    sec = 1
    time.sleep(sec)

def loop_probe():
    hash_wait()
    while True:
        probe()
        gevent.sleep(PERIOD)


def hello_world(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    yield '<b>Hello world!</b>\n'

def serve():
    print 'start serve...'
    server = pywsgi.WSGIServer(('', 8080), hello_world)
    server.serve_forever()

def http_time(url, headers = {}):
    req = urllib2.Request(url, headers = headers)
    start = time.time()
    t = HTTP_TIMEOUT
    try:
        resp = urllib2.urlopen(req, timeout=HTTP_TIMEOUT)
        resp.read()
        t = time.time() - start
    except: #  any exception: urllib2.URLError, socket.error, etc
        pass
    return (t, url)

def probe():
    print 'start probe...'
    ips = [ '103.192.253.225', '222.222.207.9','123.123.123.123']
    headers = { "Host": FAKE_HOST}
    jobs = [gevent.spawn(http_time, 'http://%s:%s/2M.dat' %(ip, UP_PORT), headers) for ip in ips]
    gevent.joinall(jobs, timeout=PROBE_TIMEOUT)
    print [job.value for job in jobs]


if __name__ == '__main__':
    gevent.signal(signal.SIGQUIT, gevent.kill)
    gevent.joinall([
        gevent.Greenlet.spawn(loop_probe),
        gevent.spawn(serve)
    ])
