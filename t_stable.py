#!/usr/bin/env python
# encoding: utf-8
import math
import random


def stable_1(series):
    dic = {}
    max_i = None
    for i in series:
        dic.setdefault(i, 0)
        dic[i] += 1
        k, _ = max_k(dic)
        if k != max_i:
            print 'leader changed to:', k
            max_i = k


def stable_2(series):
    """
    series: [A,B,A,A,...]
    stable by 2**times
    """
    dic = {}
    leader = None
    for i in series:
        dic.setdefault(i, 0)
        dic[i] += 1
        k, _ = max_k(dic, leader)
        if None != k and k != leader:
            print 'leader changed to:', k
            leader = k


def max_k(dic, leader=None):
    """
    dic: {k: count}
    """
    threshold = 0
    if None != leader:
        v = dic[leader]
        threshold = 2**(math.ceil(math.log(v, 2)) + 1)
        #print 'dic:', dic, 'leader: ', leader, 'v:', dic[leader], 'threshold:', threshold

    max_k = None
    for k, v in dic.iteritems():
        if k == leader:
            continue
        if v > threshold:
            #print 'k: %s, v: %s, threshold: %s' %(k, v, threshold)
            max_k, threshold = k, v
    #print max_k, threshold
    return max_k, threshold


def toss():
    return random.randint(0, 1)


def test_stable(n=1000):
    lst = [toss() for i in range(1000)]
    print 'stable_1:'
    stable_1(lst)
    print 'stable_2:'
    stable_2(lst)


import copy

min_c = 3
max_c = 720 # latest half day


def rank_nodes(dic_nodes):
    """
    dic_nodes: {node_i: {1:3, 2:1}}
    """
    while dic_nodes:
        limit_n, min_node = min([(sum(scores.values()), n) for (n, scores) in dic_nodes.iteritems()])
        best = evaluate(dic_nodes, limit_n)
        if best != min_node:
            # re evalutate
            best = evaluate(copy.copy(dic_nodes).pop(min_node))
        dic_nodes.pop(best)


def evaluate(dic_nodes, limit_n):
    for n, scores in dic_nodes.iteritems():
        if len(scores) > limit_n:
            score_n = sorted(scores)[:limit_n]
    best = best(nodes)
    return best

from collections import defaultdict

def pop_ranks(orders):
    dic = defaultdict(int)
    for r in orders:
        dic[r[0]] += 1
    return dic


def add_up(orders):
    """
    to compress data size
    >>> orders = [\
            ['A','B','C','D'],\
            ['A','C','B','D'],\
            ['B','A','C'],\
            ['E','A','B']\
        ]
    >>> assert add_up(orders) == {\
            'A':{0:2, 1:2},\
            'B':{0:1, 1:1, 2:2},\
            'C':{1:1, 2:2},\
            'D':{3:2},\
            'E':{0:1}\
        }
    """
    dic_nodes = defaultdict(lambda: defaultdict(int))
    for order in orders:
        for i, n in enumerate(order):
            dic_nodes[n][i] += 1
    return dic_nodes


def count_rank(dic_nodes, index=0):
    """
    >>> dic_nodes = {'A': {0:3, 1:2}, 'B':{0:2, 1:3}, 'C':{1:2, 2:1}}
    >>> assert count_rank(dic_nodes) == {'A': 3, 'B': 2}
    >>> assert count_rank(dic_nodes, 1) == {'A': 2, 'B': 3, 'C': 2}
    """
    res = {}
    for n, scores in dic_nodes.iteritems():
        for i in scores:
            if i == index:
                res[n] = scores[i]
                break
    return res


# TODO
def save():
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    #  test_stable()

