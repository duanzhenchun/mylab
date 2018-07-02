# coding=utf8
import os
import re
import jieba
import jieba.posseg as pseg
from collections import defaultdict
import sys
import codecs
sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)


pattern = re.compile(u'[\u4e00-\u9fa5]+')

f1name = 'xiyou2.txt'

def to_unicode(s):
    if type(s) != unicode:
        s = s.decode('utf8', 'ignore')
    return s


def gen_sentence(fname, encoding='utf8'):
    for l in codecs.open(fname, encoding=encoding):
        for sen in pattern.findall(to_unicode(l.strip())):
            yield sen

def gen_cs(fname, encoding='utf8'):
    for sen in gen_sentence(fname, encoding):
        for w in jieba.cut(sen):
            yield w

def gen_ngram(iter, n=2):
    while True:
        res=[]
        for i in range(n):
            t=iter.next()
            if not t:
                return
            res.append(t)
        yield ''.join(res)


def gen_ngrams(iter):
    res=[]
    while True:
        t = iter.next()
        if None == t:
            return
        if t in dic:
            res.append(t)
        elif res:
            yield ''.join(res)
            res=[]

dic = defaultdict(int)
dic2 = defaultdict(int)

stops = set()
for i in open('stop-words_chinese_1_zh.txt'):
    stops.add(to_unicode(i.strip()))

for w in gen_ngram(gen_cs(f1name)):
    if w in stops:
        continue
    dic[w] += 1

folder = './srt/'
for fname in os.listdir(folder):
    if not fname.endswith('.txt'):
        continue
    for w in gen_ngram(gen_cs(folder + fname)):    #, 'gb18030'):
        dic2[w] += 1

res = sorted(dic2.iteritems(), key=lambda (k, v): v, reverse=True)
for i in res[:200]:
    print i[0], i[1]
