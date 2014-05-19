# coding=utf-8

import cgi, urlparse, datetime, time, traceback
import dateutil
import math
import time
import re
from conf import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger


def time2now(created_at):
    return time.time() - time.mktime(get_create_at(created_at).timetuple())
    
def benchmark(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print '%s %f %s' % (f.__name__, time.time() - t, 'sec')
        return res
    return wrapper

def tounicode(s):
    return isinstance(s, unicode) and s or isinstance(s, int) and unicode(s) or s.decode('utf-8')

def toutf8(s):
    return isinstance(s, unicode) and s.encode('utf-8') or isinstance(s, int) and str(s) or s


def normalize(lst):
    total = float(sum(lst))
    if total <= 0:
        return lst
    else:
        return [i / total for i in lst]

def entropy(f):
    '''Takes a frequency and returns -1*f*log(f,2)'''
    return -1 * f * math.log(f, 2)




def sample_rotation(N, ratio=.25):
    def split_sample():
        for i in range(int(1 / ratio)):
            loc = map(lambda x:int(x * N * ratio), (i, i + 1))  
            yield loc
    def multirange():
        for i in xrange(0, loc[0]):
            yield i 
        for i in xrange(loc[1], N):  
            yield i  
    for loc in split_sample():
        yield multirange(), xrange(*loc)


def lstclosure():
    lst=[]
    def _(x=None):
        if x:
            lst.append(x)
        else:
            return lst
    return _

def get_querymid(url):
    return url.split('/')[-1].split('#')[0]

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]
