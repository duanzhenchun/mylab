#!/usr/bin/env python
# coding=utf-8
# refer jieba
import math
import re

# \u4E00-\u9FD5a-zA-Z0-9+#&\._ : All non-space characters. Will be handled with re_han
# \r\n|\s : whitespace characters. Will not be handled.
re_han = re.compile(ur"([\u4E00-\u9fA5-zA-Z0-9+#&\._%]+)")
re_skip = re.compile(ur"(\r\n|\s)")


def gen_word(fname):
    with open(fname) as f:
        for lineno, line in enumerate(f, 1):
            try:
                line = line.strip().decode('utf-8')
                word, freq = line.split(' ')[:2]
                yield word, int(freq)
            except ValueError:
                raise ValueError(
                    'invalid dictionary entry in %s at Line %s: %s' %
                    (fname, lineno, line))


def build_pfdict(fname):
    # use diction to store prefix info
    lfreq = {}
    ltotal = 0
    for word, freq in gen_word(fname):
        lfreq[word] = freq
        ltotal += freq
        for r in xrange(1, len(word) + 1):
            wfrag = word[:r]
            if wfrag not in lfreq:
                lfreq[wfrag] = 0  # speed up DAG by add pref = 0 to lfreq
    return lfreq, ltotal


def cut2words(sentence, lfreq, ltotal):
    cut_block = __cut_DAG
    for blk in re_han.split(sentence):
        if not blk:
            continue
        if re_han.match(blk):
            for word in cut_block(lfreq, ltotal, blk):
                yield word
        else:
            tmp = re_skip.split(blk)
            for x in tmp:
                if re_skip.match(x):
                    yield x
                else:
                    for xx in x:
                        yield xx


def __cut_DAG(lfreq, total, sentence):
    DAG = get_DAG(lfreq, sentence)
    route = calc(lfreq, total, sentence, DAG)
    x = 0
    buf = ''
    while x < len(sentence):
        y = route[x][1] + 1
        l_word = sentence[x:y]
        if y - x == 1:
            buf += l_word
        else:
            if buf:
                for w in gen_buf_w(buf):
                    yield w
                buf = ''
            yield l_word
        x = y
    if buf:
        for w in gen_buf_w(buf):
            yield w


def gen_buf_w(buf):
    # print 'gen_buf_w', buf
    if buf:
        if len(buf) == 1:
            yield buf
        else:
            for elem in buf:
                yield elem


def get_DAG(lfreq, sentence):
    DAG = {}        # {k: [lst]}, k: start pos < lst: all word end pos
    N = len(sentence)
    for k in xrange(N):
        lst = []    # dict word position list
        i = k
        frag = sentence[k]
        while i < N and frag in lfreq:  # speedup by lfreq[prefix]==0
            if lfreq[frag]:
                lst.append(i)
            i += 1
            frag = sentence[k:i + 1]
        if not lst:
            lst.append(k)
        DAG[k] = lst
    return DAG


def calc(lfreq, total, sentence, DAG):
    N = len(sentence)
    route = {N: (0, 0)}     # {start_pos: (max_freq_product, end_pos)}
    logtotal = math.log(total)
    for idx in xrange(N - 1, -1, -1):
        route[idx] = max((math.log(lfreq.get(sentence[idx:x + 1]) or 1) - logtotal + route[x + 1][0], x)
                         for x in DAG[idx])
    return route


samples = [
    u'改判被告人死刑立即执行',
    u'检察院鲍绍坤检察长',
    u'小明硕士毕业于中国科学院计算所',
    u'工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作',
]


if __name__ == '__main__':
    fname = '/usr/local/lib/python2.7/site-packages/jieba/dict.txt'
    lfreq, ltotal = build_pfdict(fname)
    sentence = u'看那一片白云'
    for sentence in samples:
        print '|'.join([w for w in cut2words(sentence, lfreq, ltotal)])
