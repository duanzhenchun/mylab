#!/usr/bin/env python
# encoding: utf-8
import math
import random
from collections import defaultdict


def stable_1(series):
    dic = {}
    max_i = None
    for i in series:
        dic.setdefault(i, 0)
        dic[i] += 1
        k = max_k(dic)
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
    #  print 'max_k', 'dic:', dic, 'leader:', leader
    threshold = 0
    if None != leader and leader in dic:
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
    if not max_k:
        max_k = leader
    return max_k


def toss():
    return random.randint(0, 1)


def test_stable(n=1000):
    lst = [toss() for i in range(1000)]
    print 'stable_1:'
    stable_1(lst)
    print 'stable_2:'
    stable_2(lst)


def rank_nodes(orders, last_rank=[]):
    """
    reurn sorted nodes by rank: [A,C,B,...]
    """
    ranks = []
    while orders:
        candidates = set(orders[-1])
        leaders = lead_count(orders, candidates)
        #  print 'leaders:', leaders
        # supply new node by 2**count
        leader_n = orders[-1][0]
        supply_i = 0
        for order in orders:
            if leader_n not in order:
                supply_i += 1
        #  print 'node: %s, supply_i: %s' %(leader_n, supply_i)
        if supply_i > 0:
            leaders[leader_n] += 2**supply_i
        leader = last_rank and last_rank[0] or None
        k = max_k(leaders, leader)
        #  print 'leader:', k
        leader = k
        try:
            last_rank.remove(leader)
        except:
            pass
        ranks.append(leader)
        orders = remove_node(orders, leader)
    return ranks

def remove_node(orders, node):
    new_orders = []
    for o in orders:
        try:
            o.remove(node)
        except:
            pass
        if o:
            new_orders.append(o)
    return new_orders


def test_rank():
    import copy
    orders = []
    rank = []
    for data in (
            ['A', 'B', 'C', 'D'],
            ['A', 'C', 'B', 'D'],
            ['B', 'A', 'C'],
            ['E', 'A', 'B']
        ):
        print 'data:', data
        orders.append(data)
        rank = rank_nodes(copy.deepcopy(orders), rank)
        print 'rank:', rank


def lead_count(orders, candidates):
    #  print 'lead_count', 'orders:', orders,'candidates:',  candidates
    dic = defaultdict(int)
    for r in orders:
        if r and r[0] in candidates:
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
    test_rank()
