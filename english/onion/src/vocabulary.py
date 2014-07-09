import os
import tempfile
import marshal
import ast
from db import * 
from utils import *

Default_cache = os.path.join(tempfile.gettempdir(), 'en_word_freq.cache')
Fdata = '../data'

#from nltk.stem import WordNetLemmatizer
#Wnl = WordNetLemmatizer()
from nltk.stem.porter import PorterStemmer
ST = PorterStemmer()

def word_lem(w):
    w = w.lower()
    w = Mem.hget(K_uk, w) or w
    if Mem.hexists(K_encs, w):
        wd = w
    else:
        wd = ST.stem(w)
    return wd

def t_wordlem():
    ws = 'brothers bulked Guard shrieking dressed debating'
    res=[word_lem(w) for w in ws.split()]
    print ' '.join(res)

def set_freq(w, v):
    Mem.hset(K_freq, w, v)

def get_freq(w):
    try:
        return int(Mem.hget(K_freq, w))
    except:
        return 0

def get_K(uid):
    res = Mem.hget(K_K, uid)
    if res:
        return ast.literal_eval(res)
    else:
        K = get_freq(Word0)
        return K,0


def set_K(K, uid, n):
    Mem.hset(K_K, uid, (K,n))
    print 'new K:%s, n: %d' %(K,n)


@benchmark
def prepare(fname=Default_cache):
    failed = True
    if os.path.exists(fname):
        try:
            wdict, dic_uk = marshal.load(open(fname, 'rb'))
            failed = False
        except Exception, e:
            print e
    if failed:
        dic_uk = uk_us()
        wdict = init_dict()
        dump_dicts(wdict, dic_uk)
    print 'english dict len: %d' % len(wdict)
    to_mem(wdict, dic_uk, Uid0)

@benchmark
def to_mem(wdict, dic_uk, uid):
    for w, v in wdict.iteritems():
        Mem.hset(K_freq, w, v)
    for uk, us in dic_uk.iteritems():
        Mem.hset(K_uk, uk, us)
    K = wdict.get(word_lem(Word0))
    print "K:%d" % K
    Mem.hset(K_K, uid, (K,0))

@benchmark
def to_marshal():
    wdict = Mem.hgetall(K_freq)
    dic_uk = Mem.hgetall(K_uk) 
    dump_dicts(wdict, dict_uk)

@benchmark
def dump_dicts(wdict, dict_uk, fname=Default_cache):
    import random
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


@benchmark
def init_dict():
    fname='%s/all.num' %Fdata
    f = open(fname)
    lst = f.readlines()
    dic = {}
    for l in lst:  #from easy to hard
        t = l.strip().split(' ')
        w = word_lem(t[1])
        if w in dic:
            continue
        dic[w] = int(t[0])
    return dic


@benchmark
def uk_us():
    # http://www.tysto.com/uk-us-spelling-list.html
    uk_f, us_f = (open('%s/%s.txt' %(Fdata, i)) for i in ('uk','us'))
    dic = {}
    for uk, us in zip(uk_f, us_f):
        dic[uk.strip()] = us.strip()
    return dic


# as zipf-law, if rank(w)>1000 and freq(w)>10: rank * freq = C
Usual_wfreq=(4, 7600)

def update_freq(w0, unknown, uid, ncache=10):
    w = word_lem(w0)
    v = get_freq(w)
    K, n = get_K(uid)
    if v <= 0 and not Mem.hexists(K_encs, w): #word freq not recorded
        return 
    elif unknown and 0<v<K: #neglect
        return
    name = K_cache %uid
    if not unknown:
        vcache = Mem.hget(name, w)
        if vcache:
            # rollback cache word
            freq, _ = ast.literal_eval(vcache)
            set_freq(w, freq)
            Mem.hdel(name, w)
            return
    set_freq(w, unknown and K-1 or K+1) #pre-set

    print 'set cache:', w, v, unknown
    Mem.hset(name, w, (v, unknown))
    # flush cache
    if Mem.hlen(name)>=ncache:
        lst = []
        for w, v in Mem.hgetall(name).iteritems():
            v, unknown = ast.literal_eval(v)
            if v < Usual_wfreq[0] or v > Usual_wfreq[1]:
                continue 
            if v>K*4 or v<K/4:  #neglect (1/4, 4) change of K
                continue
            lst.append(1.0/v)
        a = 1.0/K 
        if lst:
            ncut=n>4 and 4 or n
            a = (a * ncut + sum(lst)/len(lst)) /(ncut+1)
        newK = max(1, int(1.0/a))
        n = min(n+1, 10**6)    #assume user do not update to this big 
        set_K(newK, uid, n)
        for w, v in Mem.hgetall(name).iteritems():
            _, unknown = ast.literal_eval(v)

            if n>=10:   #reliable user
                set_freq(w, unknown and K-1 or K+1)
            else:       #new user
                vnew = 2./(1./K + 1./v)
                set_freq(w, vnew)
        Mem.delete(name)


def test_zipf(wdict):
    from matplotlib import pyplot as plt
    lst = sorted(wdict.values(), reverse=True)
    plt.loglog(lst)
    plt.show()

def stats():
    from matplotlib import pyplot as plt

    Diff={}
    for w in wdict:
        try:
            v = int(Mem.hget(K_freq, w))
        except:
            print w, v
        if wdict[w] != v:
            Diff[w]=[wdict[w],v]
    res=sorted(Diff.iteritems(), key=lambda (w,v):v[0])
    f=open('../data/Diff.txt','w')
    for w,vs in res:
        f.write('%s: %s, %s\n' %(w, vs[0],vs[1]))
    f.close()
    ys=Diff.values()
    plt.scatter(*zip(*ys))
    plt.show()


if __name__ == '__main__':
    #prepare()
    pass
