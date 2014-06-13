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
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger


def time2now(created_at):
    return time.time() - time.mktime(get_create_at(created_at).timetuple())

def now_timestamp():
    return int(time.time())

def fmt_timestamp(t):
    dt = datetime.datetime.fromtimestamp(t)
    return dt.strftime('%Y-%m-%d %H:%M')

def benchmark(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print '%s %f %s' % (f.__name__, time.time() - t, 'sec')
        return res
    return wrapper


def get_encoding(txt):
    return chardet.detect(txt[:100])['encoding']

def tounicode(s):
    encoding = get_encoding(s)
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


def get_curpage(request):
    try:
        page = max(1, int(request.GET.get("page", 1)))
    except ValueError:
        page = 1
    return page

def get_page_content(request, allcount, page_size, cur):
    paginator = Paginator([[] for _ in xrange(allcount)], page_size)
    after_range_num = 6
    bevor_range_num = 5
    try:
        pagelist = paginator.page(cur)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        pagelist = paginator.page(1)
        cur = 1
 
    if cur >= after_range_num:
        page_range = paginator.page_range[
            cur - after_range_num:cur + bevor_range_num]
    else:
        page_range = paginator.page_range[0:int(cur) + bevor_range_num]

    # 对get的地址进行解析
    addr = request.META['QUERY_STRING']
    addr = '&'.join(
        [i for i in addr.split('&') if i.split('=')[0] not in ['page', 'url']])
    addr = '&'.join([addr, 'page'])
    return pagelist, page_range, addr


