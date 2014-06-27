# coding=utf-8

import cgi
import urlparse
import datetime
import time
import traceback
import chardet
import math
import time
import re
from conf import *

Sent_join= re.compile(u'(?<=[\w,][—\-\s])\n(?=\w)')

def fit_urlpath(fname):
    return re.match('^[\w\.]+$', fname)

def to_lines(txt):
    txt = tounicode(txt, 'utf8')
    return Sent_join.sub('', txt).split('\n')


def time2now(created_at):
    return time.time() - time.mktime(get_create_at(created_at).timetuple())

def now_timestamp():
    return int(time.time())

def fmt_timestamp(t, year=False):
    dt = datetime.datetime.fromtimestamp(t)
    return dt.strftime((year and '%Y-' or '') + '%m-%d %H:%M')

def benchmark(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print '%s %f %s' % (f.__name__, time.time() - t, 'sec')
        return res
    return wrapper


def get_encoding(txt):
    return chardet.detect(txt[:100])['encoding']

def tounicode(s, encoding=None):
    if not encoding:
        encoding = get_encoding(s) or 'utf8'
    return isinstance(s, unicode) and s or s.decode(encoding, 'ignore') 


def toutf8(s):
    return isinstance(s, unicode) and s.encode('utf8') or s


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
            loc = map(lambda x: int(x * N * ratio), (i, i + 1))
            yield loc

    def multirange():
        for i in xrange(0, loc[0]):
            yield i
        for i in xrange(loc[1], N):
            yield i
    for loc in split_sample():
        yield multirange(), xrange(*loc)


def lstclosure():
    lst = []

    def _(x=None):
        if x:
            lst.append(x)
        else:
            return lst
    return _


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def get_querymid(url):
    return url.split('/')[-1].split('#')[0]


def gen_part(txt, psize=2500, most=20):
    l,r=0,psize
    while l<len(txt):
        more = r+most
        for i in (' ', '\n'):
            pos = txt.find(i, r, more) 
            if pos <=0:
                continue
            else:
               more=min(pos, more)
        r=more+1
        yield txt[l:r]
        l,r=r,r+psize

#string.digits, string.uppercase
Numerals = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def baseN(num,b):
        return ((num == 0) and Numerals[0]) or (baseN(num // b, b).lstrip(Numerals[0]) + Numerals[num % b])


def n36s(n):
    return baseN(n, 36)

def s36n(s):
    return int(s, 36)

