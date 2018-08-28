#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict

N = 10**5  # total url
# assume hot_url theshold = 60qps, 60 machines, 40k qps/machine
qps = 40000
max_qps = 1000
max_size = 1000  # of dic: {key:count}
top_n = 100     # assume cold url's qps < 1
epochs = 60
period = 5
MAX_C = 5 * 60
n_batch = 500


def longtail_pdf():
    a, b = max_qps, 0.07
    x = np.arange(N)
    y = a * np.exp(-b * x)
    print 'threshold: y[%s]=%.1f' % (top_n, y[top_n])
    y /= y.sum()
    # plt.plot(x, y)
    # plt.show()
    return x, y


def reduce_count(dic, to_cut, n):
    to_cut.clear()
    for k in dic:  # as url key
        dic[k] -= n
        if dic[k] <= 0:
            to_cut.add(k)
        else:
            dic[k] = min(MAX_C, dic[k])
    print 'reduce_count: %d' % len(to_cut)
    for k in to_cut:
        del dic[k]


def simulate(x, y, dic):
    n_avail = max_size - len(dic)
    print 'len(dic):', len(dic), 'n_avail:', n_avail
    if n_avail <= 0:
        return
    # a = np.array([])
    for _ in xrange(qps / n_batch):
        # fake work...
        # simulate url frequency, hot url has higher hit possibility
        ks = np.random.choice(x, size= n_avail / (qps / n_batch), p=y)
        for k in ks:
            dic[k] += 1


def sort_by_v(dic, reverse=True):
    return [
        k for (k, v) in sorted(
            dic.iteritems(), reverse=reverse, key=lambda (k, v): v)
    ]


if __name__ == "__main__":
    dic = defaultdict(int)
    x, y = longtail_pdf()
    # initial dic
    ks = np.random.choice(x, size = max_size)
    for k in ks:
        dic[k] += 1

    to_cut = set()
    for i in range(1, epochs + 1):
        simulate(x, y, dic)
        if i % period == 0:
            reduce_count(dic, to_cut, period)
    miss = 0
    for i in range(top_n):
        if i not in dic:
            miss += 1
    print 'if report all(%d), miss(<%s) = %d' % (len(dic), top_n, miss)
    c = 0
    for k in sort_by_v(dic)[:max_size]:
        if k < top_n:
            c += 1
    print 'if report %d miss=%d' % (max_size, top_n - c)
    plt.scatter(*zip(*dic.iteritems()))
    plt.show()
