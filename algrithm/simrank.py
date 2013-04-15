import numpy as np
import itertools
import networkx


def simrank(G, r=0.8, max_iter=100, eps=1e-4):
    nodes = G.nodes()
    nodes_i = {k: v for(k, v) in [(nodes[i], i) for i in range(0, len(nodes))]}

    sim_prev = np.zeros(len(nodes))
    sim = np.identity(len(nodes))

    for i in range(max_iter):
        if np.allclose(sim, sim_prev, atol=eps):
            break
        sim_prev = np.copy(sim)
        for u, v in itertools.product(nodes, nodes):
            if u is v:
                continue
            u_ns, v_ns = G.neighbors(u), G.neighbors(v)
            s_uv = sum([sim_prev[nodes_i[u_n]][nodes_i[v_n]] for u_n, v_n in itertools.product(u_ns, v_ns)])
            sim[nodes_i[u]][nodes_i[v]] = (r * s_uv) / (len(u_ns) * len(v_ns))
    print i
    return sim

"""
e.g.:

+-------+
|       |
a---b---c---d

Let's verify the result by calculating similarity between, say, node a and node b, denoted by S(a,b).
S(a,b) = r * (S(b,a)+S(b,c)+S(c,a)+S(c,c))/(2*2) = 0.9 * (0.6538+0.6261+0.6261+1)/4 = 0.6538,
which is the same as our calculated S(a,b) above.
For more details, you may want to checkout the following paper:
G. Jeh and J. Widom. SimRank: a measure of structural-context similarity. In KDD'02 pages 538-543. ACM Press, 2002.
"""

G = networkx.Graph()
G.add_edges_from([('a', 'b'), ('b', 'c'), ('c', 'a'), ('c', 'd')])
print(simrank(G))
