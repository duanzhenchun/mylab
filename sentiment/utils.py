# encoding:utf-8
import time
import logging

def sortk_iter(dic):
    return sorted(dic.iteritems())


def sortk_iter_bylen(dic, decrease=True):
    return sorted(dic.iteritems(), key=lambda (k, v):(len(k), v), reverse=decrease)


def sortv_iter(dic, reverse=False):
    for key, value in sorted(dic.iteritems(), reverse=reverse, key=lambda (k, v): (v, k)):
        yield key, value

def decode_line(l):
    if not (type(l) is unicode):
        try:
            l = l.decode('utf-8')
        except:
            l = l.decode('gbk', 'ignore')
    return l
    
def benchmark(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print '%s %f %s' % (f.__name__, time.time() - t, 'sec')
        return res
    return wrapper
