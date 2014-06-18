# coding=utf8

import re
import sys
import os
import ast
from nltk.corpus import wordnet
import Ebbinghaus
import pronounce
import vocabulary
from db import *
from utils import *


Word_pat = re.compile(u"[\w’']+|\W+")
Sep_sent = re.compile(u'(?<=[\.\?!:]) ') 
Span_name='word_span'


def word_def(w, spname=Span_name):
    ss = wordnet.synsets(w)
    if not ss:
        return w
    else:
        info = '\n'.join((ss[0].name, pronounce.show(w), ss[0].definition))
        return '<span class="%s" title="%s" >%s</span>' % (spname, info, w)


def decorate(lines, uid):
    for line in lines:
        yield ''.join(mark(line, uid))

def mark(line, uid):
    K, n = vocabulary.get_K(uid)
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

def clo_target(ncache=10):
    cdic={}
    def update(uid):
        K, n = vocabulary.get_K(uid)
        lst=[]
        for w, (v, unknown) in cdic.iteritems():
            if v < Usual_wfreq[0] or v > Usual_wfreq[1]:
                continue 
            lst.append(1.0/v)
        a = 1.0/K 
        if lst:
            a = (a * n + sum(lst)/len(lst)) /(n+1)
        newK = max(1, int(1.0/a))
        vocabulary.set_K(newK, n+1)

        for w, (v, unkwon) in cdic.iteritems():
            vocabulary.set_freq_K(w, unknown, uid)
        cdic.clear()

    def cache(w, v, unknown, uid):
        if len(cdic)<ncache:
            vocabulary.set_freq_K(w, unknown, uid) #pre-set
            cdic[w] = (v, unknown)
            print 'w:', w, 'cdic len:', len(cdic)
        else:
            update(uid)
    return cache
f_newK = clo_target()


def updateK(w, unknown, txt, uid):
    w0 = vocabulary.word_lem(w)
    v = vocabulary.get_freq(w0)
    if v < 0:
        return ''
    f_newK(w0, v, unknown, uid)
    lines = to_lines(txt)
    remember_lines(lines, w, unknown, uid)
    return decorate(lines, uid)

def remember_lines(lines, w, unknown, uid):
    for line in lines:
        for sent in Sep_sent.split(line):
            if w in sent:
                sent = mark_word(sent, w)
                remember(w, unknown, sent, uid)
                return

def remember(w, unknown, sentence, uid):
    names = (K_known, K_unknown)
    if unknown:
        names = names[::-1]
    Mem.hdel(names[1] %uid, w)
    now = now_timestamp()

    v = word_info(names[0] %uid, w)
    new_w=True
    if v:
        v [0] = sentence
        new_w=False
    else:
        v = (sentence, now, 0)
    Mem.hset(names[0] %uid, w, v)
    if unknown:
        if new_w or Mem.zrank(K_tl %uid, w) == None:
            toshow = Ebbinghaus.period[0]
            Mem.zadd(K_tl %uid, w, now + toshow)
    else:
        Mem.zrem(K_tl %uid, w)


def word_info(name, w):
    v = Mem.hget(name, w)
    if v:
        v = list(ast.literal_eval(v))
    return v
 
def repeat(w, uid):
    name= K_unknown %uid
    v =  word_info(name, w)
    if not v:
        print w, 'not found!'
        return
    v[-1]+=1
    Mem.hset(name, w, v)
    if Ebbinghaus.finished(v[-1]):
        Mem.zrem(K_tl %uid, w)
    else:
        toshow = Ebbinghaus.period[v[-1]]
        t = now_timestamp() + toshow
        Mem.zadd(K_tl %uid, w, t)

def time2wait(uid):
    wait = Ebbinghaus.period[-1]
    res = Mem.zrangebyscore(K_tl %uid, 0, sys.maxint, 0, 1, withscores=True)
    print uid, wait, res
    if res:
        w,t = res[0]
        wait = min(wait, t - now_timestamp())
    return wait

def show_unknowns(uid, n=10, debug=False):
    now = now_timestamp()
    name = K_unknown %uid
    res = Mem.zrangebyscore(K_tl %uid, 0, sys.maxint, 0, n, withscores=True)
    for (w, t) in res:
        diff = now - t 
        if not debug:
            if diff<0:
                break
        v = word_info(name, w)
        v[1] = fmt_timestamp(v[1])
        if v[-1]<0 or Ebbinghaus.finished(v[-1]):
            continue
        if diff>Ebbinghaus.period[v[-1]+1]:
            forget(w, uid)
            if not debug:
                continue
        yield w, v 


def forget(w, uid):
    name = K_unknown %uid
    v = word_info(name, w)
    v [-1] = -1
    Mem.hset(name, w, v)


def reset_wlevel():
    for w,v in Mem.hgetall(K_unknown).iteritems():
        v=list(ast.literal_eval(v))
        v[-1] = 0
        Mem.hset(K_unknown, w, v)


def mywords(uid):
    for i, name in enumerate((K_known, K_unknown)):
        name = name %uid
        dic={}
        for w in Mem.hkeys(name):
            v = word_info(name, w)
            v[1] = fmt_timestamp(v[1])
            dic[w]=v
        yield i, dic

def test_show_unkdown(): 
    uid, n = 4, 10000 
    res=Mem.zrangebyscore(K_tl %uid, 0, sys.maxint, 0, n, withscores=True) 
    for w, t in res:
        Mem.zadd(K_tl %uid, w, now)


if __name__ == "__main__":
    lines = 'Maugham remains the consummate craftsman.…[His writing is] so compact, so economical, so closely motivated, so skillfully written, that it rivets attention from the first page to last'.split(',')
    for l in decorate(lines, Uid0):
        print l
