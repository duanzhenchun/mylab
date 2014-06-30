# coding=utf8

import re
import sys
import os
import ast
import cgi
from nltk.corpus import wordnet
import Ebbinghaus
import pronounce
import vocabulary
from db import *
from utils import *


Word_pat = re.compile(u"[\w’']+|\W+")
Sep_sent = re.compile(u'(?<=[\.\?!:]) ') 
Span_name='word_span'
Pos_dict={'J':wordnet.ADJ, 'V':wordnet.VERB, 'N':wordnet.NOUN, 'R':wordnet.ADV}

def t_pos():
    """pos_tag is time-cosumming, ommit it currently."""
    from nltk.tag import pos_tag
    from nltk.tokenize import word_tokenize
    sent = "John's big idea isn't all that bad."
#    ws = word_tokenize(sent)
    ws = Word_pat.findall(sent)
    for w, pos in pos_tag(ws):
        pos = wn_pos(pos)
        ss = wordnet.synsets(w,pos)
        if not ss:
            continue
        print w, ss[0].name, ss[0].definition

    
def wn_pos(pos):
    return Pos_dict.get(pos[0],'')

def word_def0(w, spname=Span_name):
    ss = wordnet.synsets(w)
    if not ss:
        return w
    else:
        info = '\n'.join((pronounce.show(w), ss[0].definition))
        return '<span class="%s" title="%s" >%s</span>' % (spname, info, w)

def word_def(w, spname=Span_name):
    v = Mem.hget(K_encs, vocabulary.word_lem(w))
    if not v:
        return w
    else:
        info = tounicode(v, 'utf8')
        return '<span class="%s" title="%s" >%s</span>' % (spname, info, w)


def decorate(lines, uid):
    for line in lines:
        line = cgi.escape(line) #word_def will add span tag of html, so escape first
        yield ''.join(mark(line, uid))


def mark(line, uid):
    K, n = vocabulary.get_K(uid)
    for w in Word_pat.findall(line):
        if not w.isalpha() or len(w)<2:
            yield w
        else:
            w1 = vocabulary.word_lem(w)
            freq = vocabulary.get_freq(w1)
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

def updateK(w, unknown, txt, uid):
    vocabulary.update_freq(w, unknown, uid)
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
    if unknown:
        name = K_unknown %uid
        v = word_info(name, w)
        if not v:
            v = (sentence, 0)
            Mem.hset(name, w, v)
            memo(w, uid)
    else:
        Mem.hdel(K_unknown %uid, w)
        Mem.zrem(K_tl %uid, w)

def memo(w, uid):
    now = now_timestamp()
    toshow = Ebbinghaus.period[0]
    name = K_tl %uid
    if Mem.zcard(name)>Limit_memo:
        oldest = Mem.zrange(name, 0,0)[0]
        print 'remove oldest:', oldest
        Mem.zrem(name, oldest)
        Mem.hdel(K_unknown %uid, oldest)
    Mem.zadd(K_tl %uid, w, now + toshow)


def word_info(name, w):
    v = Mem.hget(name, w)
    if v:
        v = list(ast.literal_eval(v))
    return v
 
def repeat(w, uid):
    name= K_unknown %uid
    v =  word_info(name, w)
    v[-1]+=1
    Mem.hset(name, w, v)
    if Ebbinghaus.finished(v[-1]):
        Mem.zrem(K_tl %uid, w)
    else:
        toshow = Ebbinghaus.period[v[-1]]
        t = now_timestamp() + toshow
        Mem.zadd(K_tl %uid, w, t)


def time2wait(uid):
    start = now_timestamp()
    wait = Ebbinghaus.period[-1]
    res = Mem.zrangebyscore(K_tl %uid, start, start + wait, 0, 1, withscores=True)
    if res:
        wait = res[0][-1] - start
    return wait


def show_unknowns(uid, n=10):
    now = now_timestamp()
    name = K_unknown %uid
    res = Mem.zrange(K_tl %uid, 0, n-1, withscores=True)
    for (w, t) in res:
        diff = now - t 
        if diff<0:
            break
        v = word_info(name, w)
        if v[-1]<0 or Ebbinghaus.finished(v[-1]):
            Mem.zrem(K_tl %uid, w)
            continue
        if diff>Ebbinghaus.period[v[-1]+1]:
            forget(w, uid)
            continue
        yield w, v+[t]

def show_forgotten(uid, n=10):
    name = K_forget %uid
    ws = Mem.hkeys(name)[:n]
    for w in ws:
        v = Mem.hget(name, w)
        yield w, list(ast.literal_eval(v))


def forget(w, uid):
    name = K_unknown %uid
    v = word_info(name, w)
    v [-1] = -1
    if Mem.hlen(K_forget %uid)<=Limit_forget:
        Mem.hset(K_forget %uid, w, v)
    else:
        #for simplicity
        print w, 'forget limit reached'    
    Mem.hdel(name, w)
    Mem.zrem(K_tl %uid, w)


def rescue(w, uid):
    name = K_forget %uid
    v=word_info(name, w)
    Mem.hdel(name, w)
    if Mem.hexists(K_unknown %uid, w):   #may be remembered again
        return
    v[-1] = 0
    Mem.hset(K_unknown %uid, w, v)
    memo(w, uid)


def reset_wlevel(uid):
    name = K_unknown %uid
    for w,v in Mem.hgetall(name).iteritems():
        v=list(ast.literal_eval(v))
        v[-1] = 0
        Mem.hset(name, w, v)


def unknowns(uid):
    name = K_unknown %uid
    dic={}
    for w in Mem.hkeys(name):
        v = word_info(name, w)
        t = fmt_timestamp(Mem.zscore(K_tl %uid, w))
        dic[w]=v+[t]
    return dic


def set_lastpage(fname, curpage, uid):
    curpage = ast.literal_eval(curpage)
    if not isinstance(curpage, int) or curpage<=0:
        return 0
    Mem.hset(K_curpage %uid, fname, curpage)

def lastpage(fname, uid):
    last = Mem.hget(K_curpage %uid, fname )
    if not last:
        last = 0
    return last


if __name__ == "__main__":
    pass
