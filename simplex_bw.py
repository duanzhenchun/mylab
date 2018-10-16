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
    S = np.array([unit.bw for unit in units], dtype=np.float)
    print 'S:', S
    q = np.array(
        [dic_nodes[nname].quota for nname in dic_nodes], dtype=np.float)
    mq = np.array(
        [dic_nodes[nname].min_quota for nname in dic_nodes], dtype=np.float)
    # best ratio is average node ratio
    B = sum([float(unit.bw) for unit in units]) / sum(q)
    print 'B: %.2f' % B
    m, n = len(units), len(dic_nodes)
    # variables
    X = np.zeros((m, n))  # bw of unit_i, node_j, sparse matrix
    A_ub = np.zeros((n, m * n))
    # constrains
    for j, nname in enumerate(dic_nodes.keys()):
        # node.min_quota <= X[:, j].sum() <= node.quota
        tmp = np.zeros((m, n))
        tmp[:, j] = 1
        A_ub[j] = tmp.flatten()
    A_ub = np.hstack((A_ub, -A_ub))  # U - V
    A_ub = np.vstack((A_ub, -A_ub))  # min_quota, quota
    # Z_ij = X_ij/q_j - B = U - V
    # X_ij = (U_ij - V_ij + B) * q_j >= 0
    b_ub1 = np.ones(n) * (1 - B)
    b_ub2 = np.array(-mq / q + B)
    b_ub3 = np.ones(m * n) * B
    A_ub3 = np.eye(m * n)
    A_ub3 = np.hstack((-A_ub3, A_ub3))
    b_ub = np.hstack((b_ub1, b_ub2))
    A_ub = np.vstack((A_ub, A_ub3))
    b_ub = np.hstack((b_ub, b_ub3))
    print 'A_ub', A_ub.shape
    print A_ub
    print 'b_ub', b_ub.shape, b_ub

    A_eq = np.zeros((m, m * n))
    for i, unit in enumerate(units):
        unit_nodes = set(relations[unit.name])
        t_bounds = []
        for j, nname in enumerate(dic_nodes.keys()):
            if nname in unit_nodes:
                t_bounds.append((0, None))
            else:
                t_bounds.append((0, 0))
        A_eq[i, n * i: n * (i + 1)] = q
    A_eq = np.hstack((A_eq, -A_eq))  # U - V
    print 'A_eq', A_eq.shape
    print A_eq
    b_eq = S - B / 1 * q.sum()
    print 'b_eq:', b_eq
    # 1 <= n_ij <= P_ij
    # 1/(sum_j(P_ij) - P_ij  + 1) <= X_ij/S_i <= P_ij / (sum_j(P_ij + 1) -1)
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
    # target: argmin(\sum(abs(Z_ij))) = argmin(\sum(U_ij-V_ij))
    c = np.ones(m * n * 2)
    bounds = [(0, None) for i in range(m * n * 2)]
    print 'bounds:', bounds
    res = linprog(c, A_ub, b_ub, A_eq, b_eq, bounds=bounds)
    print res
    # X = (U - V + B) * q
    print 'argmin:', res.fun
    print 'res.x:', res.x
    print 'quota:', q
    X_ij = get_Xij(res.x, B, q, m, n)
    print 'X_ij:', X_ij
    return X_ij


def get_Xij(x, B, q, m, n):
    X = x[:m * n] - x[m * n:] + B
    X = X.reshape(m,n) * q
    return X


def test():
    units = [
        Unit('g1', 'r1', 20),
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
    calc(units, dic_nodes, relations)


if __name__ == '__main__':
    test()
