#encoding:utf-8
import time
import chardet
import datetime
import sys

def input_pass(user):
    import getpass
    return getpass.unix_getpass("password of %s:" %user)
    
def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)

def test_signal():
    import signal
    signal.signal(signal.SIGINT, signal_handler)
    print 'Press Ctrl+C'
    signal.pause()

def benchmark(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print '%s %f %s' % (f.__name__, time.time() - t, 'sec')
        return res
    return wrapper
    
def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

def genpasswd(name, salt='whille', limit=12):
    import hashlib
    name=name.lower()
    salt=salt[::-1]
    res=hashlib.sha512(name + salt).hexdigest()
    return name + '_' + res[-5:], res[:limit]


def time2now(created_at):
    return time.time() - time.mktime(get_create_at(created_at).timetuple())


def benchmark(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print '%s %f %s' % (f.__name__, time.time() - t, 'sec')
        return res
    return wrapper


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


def get_encoding(txt):
    return chardet.detect(txt[:100])['encoding']

def tounicode(s):
    encoding = get_encoding(s)
    return isinstance(s, unicode) and s or s.decode(encoding, 'ignore') 

def toutf8(s):
    return isinstance(s, unicode) and s.encode('utf8') or s


def fmt_timestamp(t):
    dt = datetime.datetime.fromtimestamp(t)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


