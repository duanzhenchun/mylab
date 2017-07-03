#!/usr/bin/env python
# encoding: utf-8

import urllib2
from collections import defaultdict

url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/letter-recognition/letter-recognition.data'
data = []
for l in urllib2.urlopen(url): # files are iterable
    lst = l.strip().split(',')
    y, x = lst[0], [int(i) for i in lst[1:]]
    data.append((y, x))


c = defaultdict(lambda: defaultdict(int))
for y,x in data:
    c[x[0]][y] += 1

P = defaultdict(lambda: defaultdict(float))
for n in c:
    total = sum(c[n].values())
    for cha in c[n]:
        P[n][cha] = 1.0 * c[n][cha]/ total

from operator import itemgetter
max(enumerate(P[2].iteritems()), key=itemgetter(1))
print P[2].keys()[i]
