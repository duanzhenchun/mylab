#!/usr/bin/env python
import gevent
import time
from gevent.event import Event
from gevent.pywsgi import WSGIServer

T = 5
evt = Event()  # cross corutine
i = 1
N = 5


def main():
    called = False
    if i > 0:
        evt.wait(T)
    while True:
        start = time.time()
        called = work(called)
        print 'time elapse %.3f' %(time.time() - start)


def work(called):
    evt.clear()
    dig()
    if not called:
        print 'work as master'
        detect()
        for j in range(i, N + 1):
            call_slave(j)
    else:
        get_master()
    write_file()
    call_client()
    return evt.wait(T)


def dig():
    print 'dig domains'


def detect():
    print 'detect'


def write_file():
    print 'write_file'


def call_client():
    print 'system_call client'


def get_master():
    print 'get sync_data from master %s' %i


def call_slave(j):
    print 'call slave', j


def wakeup():
    print 'wakeup port 6210 /call with passwd protected'
    evt.set()


def ajax_endpoint(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/html')]
    start_response(status, headers)
    yield 'ok'
    wakeup()


if __name__ == '__main__':
    gevent.spawn(main)
    WSGIServer(('', 8000), ajax_endpoint).serve_forever()
    main()
