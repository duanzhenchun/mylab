import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 3), (1, 4), (4, 5)])
G2 = nx.generators.random_graphs.fast_gnp_random_graph(10, .3)
# nx.adjacency_matrix(G)
L = nx.laplacian(G)  # L=D-A
# np.linalg.eigvals(L)
np.linalg.eig(L)
res = nx.laplacian_spectrum(G)
print res

print nx.normalized_laplacian(G)
c = nx.communicability(G)

# drawing
nx.draw(G)  # default using spring_layout: force-directed
# same as:
# pos = nx.spring_layout(G)
# nx.draw(G, pos)
nx.draw_random(G)
nx.draw_spectral(G)
plt.show()
plt.savefig('path.png')
plt.cla()

# random graph
G = nx.generators.random_graphs.random_regular_graph(6, 50)
plt.show()
nx.draw(G)

def t_unionG():
    
    Gs = [ nx.generators.random_graphs.random_powerlaw_tree(10) for i in range(2)]
    G = nx.union_all(Gs, rename=('a', 'b'))
    print G.edge
    G.add_edge('a5', 'b4')
    nx.draw(G)
    plt.show()

