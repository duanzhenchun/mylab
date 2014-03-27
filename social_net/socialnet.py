import networkx as nx
import matplotlib.pyplot as plt
import random


def run(edges, show=False):
    G=nx.DiGraph()
    #G.add_weighted_edges_from([('A','B',0.5),('A','C',0.5)])
    G.add_edges_from(edges)
    if show:
        nx.draw(G, pos=nx.spring_layout(G))
        plt.show()
        nx.write_dot(G,'./graph.dot')
        # dot -n -Tpng graph.dot >graph.png
    print nx.hits(G,max_iter=10**3) #tol=1e-4)
    print nx.pagerank(G)

def perform(N=4):
    G=nx.gnp_random_graph(10**N, 1e-4, directed=True)
    print G.size()
    res=nx.pagerank(G)
    plt.plot(sorted(res.values(),reverse=True))
    plt.show()
    

def main():
    edges = link()
    run(edges, True)

def t_data():
    return [(1,2),(1,3),(1,4),(2,3),(3,4),(2,1),(4,4)]

def link():
    return [(i, i+1) for i in xrange(10)]

def repost1():
    edges=[]
    for i in xrange(1, 10):
        edges.append((i, 0))
    edges.append((0, 10))
    return edges

def repost2(start=0, n=10):
    assert n > 2
    edges = []
    for i in range(start+1,start+n):
        edges.append((i,start))
    for j in range(start+n,start+2*n):
        edges.append((j,start+1))
    return edges

def repost_andloop():
    return repost2() + [(3,3)] 

def two_cluster():
    return repost2() + repost2(50) 

def repost_vsloop():
    return repost2() + [(20,20)]

def big_small():
    return repost2() + repost2(50, n=4)
if __name__ == '__main__':
    main()
