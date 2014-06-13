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
import time
import ast
import Ebbinghaus
from db import Mem
from utils import *


log_console = logging.StreamHandler(sys.stderr)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_console)

WDict = None
Dic_uk = None
initialized = False
Word_pat = re.compile(u"[\w’']+|\W+")
ST = PorterStemmer()
Wnl = WordNetLemmatizer()
Title = ''
Content = []
Kmem = 'onion_en_known_%s'
Ktimeline = 'onion_en_timeline'
K_K = 'onion_en_K'
Init_w = 'freak'
K = 10
Sep_sent = re.compile(u'(?<=[\.\?!:]) ') 
Span_name='word_span'



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

def init_fi():
    fname = 'razors.edge.txt'
    print fname
    f=open('data/%s' %fname)
    set_article(fname, f.read())

def uk_us():
    # http://www.tysto.com/uk-us-spelling-list.html
    uk_f = open('data/uk.txt')
    us_f = open('data/us.txt')
    dic = {}
    for uk, us in zip(uk_f, us_f):
        dic[uk.strip()] = us.strip()
    return dic

def word_def(w, spname=Span_name):
    ss = wordnet.synsets(w)
    if not ss:
        return w
    else:
        definition = '%s:\n%s' % (ss[0].name, ss[0].definition)
        return '<span class="%s" title="%s" >%s</span>' % (spname, definition, w)


def init():
    global WDict, Dic_uk, initialized, K
    if initialized:
        return
    init_fi()
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
    init_K()
    initialized = True

def init_K():
    global K
    try:
        K = int(Mem.get(K_K))
    except:
        K = WDict.get(word_lem(Init_w))
    print "K:%d" % K


def set_article(fname, txt):
    global Title, Content
    Title = fname
    Content = tounicode(txt).split('\n')

def title():
    return Title

def cur_txt(cur, page_size):
    global Content
    l = page_size * (cur - 1)
    r = l + page_size
    return Content[l:r]


def decorate(lines):
    for line in lines:
        yield ''.join(mark(line))


def mark(line):
    for w0 in Word_pat.findall(line):
        if not w0.isalpha():
            yield w0
        else:
            w = word_lem(w0)
            if w in WDict and WDict[w] <= K:
                yield word_def(w0)
            else:
                yield w0

def mark_word(line, w):
    aim = word_def(w, 'mark_word')
    pat = '(?<!\w)%s(?!\w)' %w
    return aim.join(re.split(pat, line))


def clo_target(n=10):
    cache_dic={}
    def update():
        global K
        a=1.0/K
        for w, (v, unkown) in cache_dic.iteritems():
            # as zipf-law, if rank(w)>1000 and freq(w)>10: rank * freq = C
            if v < 5 or v > 7600:
                continue 
            a+= 1.0/v
        K = max(2, int((len(cache_dic)+1)/a))
        print 'new K:%s' %K
        Mem.set(K_K, K)
        for w, (v, unkwon) in cache_dic.iteritems():
            WDict[w] = unkown and K-1 or K+1
        cache_dic.clear()

    def cache(w, v, unkown):
        global K
        #pre-update w-freq
        WDict[w] = unkown and K-1 or K+1
        if len(cache_dic)<n:
            cache_dic[w] = (v, unkown)
            print 'w:', w, 'cache_dic len:', len(cache_dic)
        else:
            update()
    return cache
f_newK = clo_target()


def updateK(w, unkown, cur, page_size):
    w0 = word_lem(w)
    v = WDict.get(w0)
    if v < 0:
        return ''
    f_newK(w0, v, unkown)
    lines = cur_txt(cur, page_size)
    remember_lines(lines, w, unkown)
    return decorate(lines)

def remember_lines(lines, w, unkown):
    for line in lines:
        for sent in Sep_sent.split(line):
            if w in sent:
                sent = mark_word(sent, w)
                remember(w, unkown, sent)
                return

def remember(w, unkown, sentence):
    t = not unkown and 1 or 0
    name = Kmem % t
    name0 = Kmem % (1 - t)
    Mem.hdel(name0, w)
    v = word_info(name, w)
    now = now_timestamp()
    if v:
        v [0] = sentence
    else:
        v = (sentence, now, 0)
    Mem.hset(name, w, v)
    if unkown:
        if not v or Mem.zrank(Ktimeline, w) == None:
            toshow = Ebbinghaus.period[0]
            Mem.zadd(Ktimeline, w, now + toshow)


def word_info(name, w):
    v = Mem.hget(name, w)
    if v:
        v = list(ast.literal_eval(v))
    return v
 

def repeat(w):
    name= Kmem %0
    v =  word_info(name, w)
    if not v:
        print w, 'not found!'
        return
    v[-1]+=1
    Mem.hset(name, w, v)
    if Ebbinghaus.finished(v[-1]):
        Mem.zrem(Ktimeline, w)
    else:
        toshow = Ebbinghaus.period[v[-1]]
        Mem.zadd(Ktimeline, w, now_timestamp() + toshow)


def unkowns_toshow(debug=True):
    start ,step = 0, 20
    now = now_timestamp()
    name = Kmem %0
    res = Mem.zrangebyscore(Ktimeline, 0, sys.maxint, start, start+step, withscores=True)
    for (w, t) in res:
        diff = now - t 
        print 'w=%s, diff=%f' %(w,diff)
        if not debug:
            if diff<0:
                break
        v = word_info(name, w)
        v[1] = fmt_timestamp(v[1])
        if Ebbinghaus.finished(v[-1]):
            continue
        if diff>Ebbinghaus.period[v[-1]+1]:
            forget(w)
            if not debug:
                continue
        yield w, v 


def forget(w):
    name= Kmem %0
    v = word_info(name, w)
    v [-1] = -1
    Mem.hset(name, w, v)


def reset_wlevel():
    name = Kmem %0
    for w,v in Mem.hgetall(name).iteritems():
        v=list(ast.literal_eval(v))
        v[-1] = 0
        Mem.hset(name, w, v)


def mywords():
    for i in range(2):
        dic={}
        name = Kmem %i
        for w in Mem.hkeys(name):
            v = word_info(name, w)
            v[1] = fmt_timestamp(v[1])
            dic[w]=v
        yield i, dic

def test_zipf():
    from matplotlib import pyplot as plt
    lst = sorted(WDict.values(), reverse=True)
    plt.loglog(lst)
    plt.show()

init()


if __name__ == '__main__':
    test('data/razors.edge.txt')
