import os
import tempfile
import marshal
from db import Mem
from utils import *


K_K = 'onion_en_K'
K_freq = 'onion_en_freq'
K_uk = 'onion_en_uk'
K_word0 = 'freak'
En_freq_cache = 'en_word_freq.cache'
Fdata = '../data'


from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
ST = PorterStemmer()
Wnl = WordNetLemmatizer()

def word_lem(w):
    w = get_us(w.lower())
    return ST.stem(Wnl.lemmatize(w))

def set_freq_K(w, unkown):
    K = get_K()
    set_freq(w, unkown and K-1 or K+1)

def set_freq(w, v):
    Mem.hset(K_freq, w, v)

def get_freq(w):
    if not Mem.hexists(K_freq, w):
        return 0
    return int(Mem.hget(K_freq, w))

def get_us(w):
    us = Mem.hget(K_uk, w)
    return us and us or w

def get_K():
    return int(Mem.get(K_K))

def set_K(K):
    print 'new K:%s' %K
    return Mem.set(K_K, K)


@benchmark
def prepare():
    fname = os.path.join(tempfile.gettempdir(), En_freq_cache)
    failed = True
    if os.path.exists(fname):
        try:
            wdict, dic_uk = marshal.load(open(fname, 'rb'))
            failed = False
        except Exception, e:
            print e
    if failed:
        wdict, dic_uk = build_cache(fname)
    print 'english dict len: %d' % len(wdict)
    to_mem(wdict, dic_uk)

@benchmark
def to_mem(wdict, dic_uk):
    for w, v in wdict.iteritems():
        Mem.hset(K_freq, w, v)
    for uk, us in dic_uk.iteritems():
        Mem.hset(K_uk, uk, us)
    k = wdict.get(word_lem(K_word0))
    print "K:%d" % k
    Mem.set(K_K, k)

@benchmark
def build_cache(fname):
    import random
    dic_uk = uk_us()
    wdict = init_dict()
    print "start dumping model to file cache %s" % fname
    tmp_suffix = "." + str(random.random())
    with open(fname + tmp_suffix, 'wb') as temp_fname:
        marshal.dump((wdict, dic_uk), temp_fname)
    if os.name == 'nt':
        import shutil
        replace_file = shutil.move
    else:
        replace_file = os.rename
    replace_file(fname + tmp_suffix, fname)
    return wdict, dic_uk

@benchmark
def init_dict():
    fname='%s/all.num' %Fdata
    f = open(fname)
    lst = f.readlines()
    dic = {}
    for l in lst[-1:0:-1]:
        t = l.strip().split(' ')
        w = word_lem(t[1])
        dic[w] = max(dic.get(w, 0), int(t[0]))
    return dic


@benchmark
def uk_us():
    # http://www.tysto.com/uk-us-spelling-list.html
    uk_f, us_f = (open('%s/%s.txt' %(Fdata, i)) for i in ('uk','us'))
    dic = {}
    for uk, us in zip(uk_f, us_f):
        dic[uk.strip()] = us.strip()
    return dic

def test_zipf(wdict):
    from matplotlib import pyplot as plt
    lst = sorted(wdict.values(), reverse=True)
    plt.loglog(lst)
    plt.show()


if __name__ == '__main__':
    #prepare()
    pass
