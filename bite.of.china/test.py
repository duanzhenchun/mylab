# coding=utf8
import os
import re
import codecs
import jieba
import jieba.posseg as pseg
from collections import defaultdict


pattern = re.compile(u'[\u4e00-\u9fa5]+')


def to_unicode(s):
    if type(s) != unicode:
        s = s.decode('utf8', 'ignore')
    return s


def gen_cs(fname, encoding='utf8'):
    for l in codecs.open(fname, encoding=encoding):
        for sen in pattern.findall(to_unicode(l.strip())):
            for w in jieba.cut(sen):
                yield w

dic = defaultdict(int)
dic2 = defaultdict(int)

stops = set()
for i in open('stop-words_chinese_1_zh.txt'):
    stops.add(to_unicode(i.strip()))

f1name = 'xiyou.txt'
for w in gen_cs(f1name):
    if w in stops:
        continue
    dic[w] += 1

folder = './srt/'
for fname in os.listdir(folder):
    if not fname.endswith('.srt'):
        continue
    print fname
    for w in gen_cs(folder + fname, 'gb18030'):
        if w in dic:
            dic2[w] += 1

res = sorted(dic2.iteritems(), key=lambda (k, v): v, reverse=True)
for i in res[:50]:
    print i[0], i[1]
