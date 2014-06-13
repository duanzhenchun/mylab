# coding=utf8

import re
import sys
import os
import ast
from nltk.corpus import wordnet
import Ebbinghaus
import pronounce
import vocabulary
from db import Mem
from utils import *


Title = ''
Content = []
Kmem = 'onion_en_known_%s'
Ktimeline = 'onion_en_timeline'

Word_pat = re.compile(u"[\w’']+|\W+")
Sep_sent = re.compile(u'(?<=[\.\?!:]) ') 
Span_name='word_span'


def set_article(fname, txt):
    global Title, Content
    Title = fname
    Content = tounicode(txt).split('\n')

@benchmark
def init_fi():
    fname = 'razors.edge.txt'
    print fname
    f=open('data/%s' %fname)
    set_article(fname, f.read())
init_fi()


def word_def(w, spname=Span_name):
    ss = wordnet.synsets(w)
    if not ss:
        return w
    else:
        info = '\n'.join((ss[0].name, pronounce.show(w), ss[0].definition))
        return '<span class="%s" title="%s" >%s</span>' % (spname, info, w)

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
    K = vocabulary.get_K()
    for w in Word_pat.findall(line):
        if not w.isalpha():
            yield w
        else:
            w0 = vocabulary.word_lem(w)
            freq = vocabulary.get_freq(w0)
            if freq and freq <= K:
                spname = Span_name
                if freq <=K/2:
                    spname += ' hard'
                yield word_def(w, spname)
            else:
                yield w


def mark_word(line, w):
    aim = word_def(w, 'mark_word')
    pat = '(?<!\w)%s(?!\w)' %w
    return aim.join(re.split(pat, line))


# as zipf-law, if rank(w)>1000 and freq(w)>10: rank * freq = C
Usual_wfreq=(4, 7600)

def clo_target(n=10):
    cdic={}
    def update():
        a=1.0/vocabulary.get_K()
        for w, (v, unkown) in cdic.iteritems():
            if v < Usual_wfreq[0] or v > Usual_wfreq[1]:
                continue 
            a+= 1.0/v
        vocabulary.set_K(max(2, int((len(cdic)+1)/a)))

        for w, (v, unkwon) in cdic.iteritems():
            vocabulary.set_freq_K(w, unkown)
        cdic.clear()

    def cache(w, v, unkown):
        #pre-set
        vocabulary.set_freq_K(w, unkown)
        if len(cdic)<n:
            cdic[w] = (v, unkown)
            print 'w:', w, 'cdic len:', len(cdic)
        else:
            update()
    return cache
f_newK = clo_target()


def updateK(w, unkown, cur, page_size):
    w0 = vocabulary.word_lem(w)
    v = vocabulary.get_freq(w0)
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
    else:
        Mem.zrem(Ktimeline, w)


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


def show_unkowns(n=10, debug=False):
    now = now_timestamp()
    name = Kmem %0
    res = Mem.zrangebyscore(Ktimeline, 0, sys.maxint, 0, n, withscores=True)
    for (w, t) in res:
        diff = now - t 
        #print 'w=%s, diff=%f' %(w,diff)
        if not debug:
            if diff<0:
                break
        v = word_info(name, w)
        v[1] = fmt_timestamp(v[1])
        if v[-1]<0 or Ebbinghaus.finished(v[-1]):
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
