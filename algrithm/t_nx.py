import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


G=nx.Graph()
G.add_edges_from([(1,2),(1,3),(2,3),(1,4), (4,5)])
G2=nx.generators.random_graphs.fast_gnp_random_graph(10,.3)
#nx.adjacency_matrix(G)
L=nx.laplacian(G) # L=D-A
#np.linalg.eigvals(L)
np.linalg.eig(L)
nx.laplacian_spectrum(G)
nx.normalized_laplacian(G)
c=nx.communicability(G)

#drawing
nx.draw(G)
nx.draw_random(G)
nx.draw_spectral(G)
plt.show()
plt.savefig('path.png')
plt.cla()

