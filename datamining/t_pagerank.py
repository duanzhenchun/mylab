import networkx as nx
G=nx.gnp_random_graph(1000,0.01,directed=True)
G.size()
%timeit nx.pagerank(G,tol=1e-10)
%timeit nx.pagerank_scipy(G,tol=1e-10)

