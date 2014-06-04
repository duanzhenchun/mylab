# coding=utf8
from nltk.corpus import wordnet
import re
from stemming.porter2 import stem
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import marshal
import logging
import tempfile
import sys
import os
import random
import redis
from utils import *


log_console = logging.StreamHandler(sys.stderr)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_console)

WDict = None
Dic_uk = None
initialized = False
Word_pat = re.compile(r"[\w’']+|\W+")
ST = PorterStemmer()
Wnl = WordNetLemmatizer()
Content = []
Mem = redis.Redis()
Kmem = 'en_known_%s'
Init_w = 'freak'
K, N = 10, 0


def word_lem(w):
    w = w.lower()
    if w in Dic_uk:
        w = Dic_uk[w]
    return ST.stem(Wnl.lemmatize(w))


def init_dict(fname='data/all.num'):
    f = open(fname)
    lst = f.readlines()
    dic = {}
    for l in lst[-1:0:-1]:
        t = l.strip().split(' ')
        w = word_lem(t[1])
        dic[w] = max(dic.get(w, 0), int(t[0]))
    return dic


def uk_us():
    # http://www.tysto.com/uk-us-spelling-list.html
    uk_f = open('data/uk.txt')
    us_f = open('data/us.txt')
    dic = {}
    for uk, us in zip(uk_f, us_f):
        dic[uk.strip()] = us.strip()
    return dic

#@benchmark
def gen_html(dic, lines, k):
    for line in lines:
        yield '<p>'
        for w0 in Word_pat.findall(line):
            if not w0.isalpha():
                yield w0
            else:
                w = word_lem(w0)
                if w in dic and dic[w] <= k:
                    yield word_def(w0)
                else:
                    yield w0
        yield '</p>'


def word_def(w):
    ss = wordnet.synsets(w)
    if not ss:
        return w
    else:
        definition = '%s:\n%s' % (ss[0].name, ss[0].definition)
        return '<span class="word_span" title="%s" >%s</span>' % (definition, w)


def init():
    global WDict, Dic_uk, initialized, K, N
    if initialized:
        return
    cache_file = os.path.join(tempfile.gettempdir(), "en_word_freq.cache")
    load_fail = True
    if os.path.exists(cache_file):
        logger.debug("loading model from cache %s" % cache_file)
        try:
            WDict, Dic_uk = marshal.load(open(cache_file, 'rb'))
            logger.debug('english dict len: %d' % len(WDict))
            load_fail = False
        except Exception, e:
            print e
    if load_fail:
        Dic_uk = uk_us()
        WDict = init_dict()
        logger.debug("dumping model to file cache %s" % cache_file)
        try:
            tmp_suffix = "." + str(random.random())
            with open(cache_file + tmp_suffix, 'wb') as temp_cache_file:
                marshal.dump((WDict, Dic_uk), temp_cache_file)
            if os.name == 'nt':
                import shutil
                replace_file = shutil.move
            else:
                replace_file = os.rename
            replace_file(cache_file + tmp_suffix, cache_file)
        except:
            logger.error("dump cache file failed.")
            logger.exception("")

    K = WDict.get(word_lem(Init_w))
    N = 1
    print "K:%d" % K
    initialized = True


def set_txt(txt):
    global Content
    Content = txt.split('\n')

#@benchmark
def api(cur, page_size):
    global K, Content
    n = len(Content)
    l = page_size * (cur - 1)
    r = l + page_size
    print 'xxx', l,r,n
    txt = ''.join(gen_html(WDict, Content[l:r], K))
    return txt, n


def newTarget(k, n, v):
    # as zipf-law, if rank(w)>1000, freq(w)>10, rank * freq = C
    if v < 10 or v > 7600:
        return k, n
    k = (n + 1) / (1.0 / k * n + 1.0 / v)
    k = k > 1 and k or 2
    return k, n + 1


def updateK(w, unkown, cur, page_size):
    global K, N
    w1 = word_lem(w)
    v = WDict.get(w1)
    if v < 0:
        return ''
    remember(w, unkown)
    K, N = newTarget(K, N, v)
    print 'K:%s, N:%s, v:%s' % (K, N, v)
    WDict[w1] = unkown and K - 1 or K + 1
    print w, w1, WDict[w1]
    txt, n = api(cur, page_size)
    return txt


def remember(w, unkown):
    t = not unkown and 1 or 0
    k1 = Kmem % t
    k2 = Kmem % (1 - t)
    print k1, w
    Mem.sadd(k1, w)
    Mem.srem(k2, w)


def personal_words():
    for i in range(2):
        k = Kmem % i
        yield i, Mem.smembers(k)


def test(fname):
    print fname
    txt = open(fname).read()
    k = WDict.get(word_lem('freak'))
    print 'k:%d' % k
    f = open('%s.html' % fname, 'w')
    f.write(to_html(''.join(gen_html(WDict, txt, k)), 'onion'))
    f.close()


def zipf():
    from matplotlib import pyplot as plt
    lst = sorted(WDict.values(), reverse=True)
    plt.loglog(lst)
    plt.show()

init()


if __name__ == '__main__':
    test('data/razors.edge.txt')
