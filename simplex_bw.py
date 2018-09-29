#!/usr/bin/env python
import numpy as np
from scipy.optimize import linprog


class Unit(object):
    def __init__(self, group, region, bw):
        self.name = (group, region)
        self.bw = bw


class Node(object):
    def __init__(self, name, max_ipn, quota, min_quota):
        self.name = name
        self.max_ipn = max_ipn
        self.quota = quota
        self.min_quota = min_quota


def calc(units, dic_nodes, relations):
    # const
    # A_j = node.quota
    q = np.array([dic_nodes[nname].quota for nname in dic_nodes], dtype=np.float)
    mq = np.array([dic_nodes[nname].min_quota for nname in dic_nodes], dtype=np.float)
    # best ratio is average node ratio
    B = sum([float(unit.bw) for unit in units])/ sum(q)
    print 'B: %.2f' % B
    m, n = len(units), len(dic_nodes)
    print 'm: %d, n: %d' %(m, n)
    # variables
    X = np.zeros((m,n))     # bw of unit_i, node_j, sparse matrix
    A_ub = np.zeros((n, m * n))
    # constrains
    for j, nname in enumerate(dic_nodes.keys()):
        # node.min_quota <= X[:, j].sum() <= node.quota
        tmp = np.zeros((m,n))
        tmp[:,j] = 1
        A_ub[j] = tmp.flatten()
    # Z_ij = X_ij/q_j - B = U - V
    # X_ij = (U_ij - V_ij + B) * q_j
    # target: argmin(\sum(abs(Z_ij))) = argmin(\sum(U_ij-V_ij))
    A_ub = np.vstack((A_ub, -A_ub))     # U - V
    print A_ub
    print 'A_ub', A_ub.shape
    b_ub1 = np.ones(n) * (1 - B)
    b_ub2 = np.array(- mq / q + B)
    b_ub = np.hstack((b_ub1, b_ub2))
    print 'b_ub', b_ub.shape, b_ub
    for i, unit in enumerate(units):
        S_i = unit.bw
        unit_nodes = relations[unit.name]
        num_i = len(unit_nodes)
        sum_ip = sum(dic_nodes[nname].max_ipn for nname in unit_nodes)
        for nname in unit_nodes:
            node = dic_nodes[nname]
            Pi = node.max_ipn
            S_i / (sum_ip - Pi + 1) <= X[i, j] <= S_i * Pi / (Pi + num_i + 1)
        S_i = sum(X[i, :])
        # print num_i, sum_ip, S_i
    c = np.ones(n * 2)
    print c.shape, A_ub.shape, b_ub.shape
    bounds = [(0, None) for i in range(n * 2)]
    res = linprog(c, A_ub, b_ub, bounds=bounds)
    # X = (U - V + B) * q
    print res.x
    print 'argmin:', res.fun
    X = res.x[:n] + res.x[n:]* -1
    X = (X + B) * q
    print X
    return res


def test():
    units = [
        Unit('g1', 'r1', 10),
        Unit('g2', 'r1', 30),
    ]
    dic_nodes = {
        'n1': Node('n1', 5, 20, 6),
        'n2': Node('n2', 5, 40, 12),
        'n3': Node('n3', 3, 30, 10),
    }
    relations = {
        ('g1', 'r1'): ('n1', 'n2'),
        ('g2', 'r1'): ('n2', 'n3'),
    }
    print calc(units, dic_nodes, relations)


if __name__ == '__main__':
    test()
