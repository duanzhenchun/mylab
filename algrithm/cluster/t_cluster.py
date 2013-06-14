#!/usr/bin/python
import numpy as np
import sklearn.cluster

    
def loaddata():
    """ 
    load previously generated points
    """
    import cPickle as pickle
    
    with open('cluster.pkl') as inf:
        samples = pickle.load(inf)
    N = 0
    for smp in samples:
        N += len(smp[0])
    X = np.zeros((N, 2))
    idxfrm = 0
    for i in range(len(samples)):
        idxto = idxfrm + len(samples[i][0])
        X[idxfrm:idxto, 0] = samples[i][0]
        X[idxfrm:idxto, 1] = samples[i][1]
        idxfrm = idxto
    return X
    
def observer(X, labels, centers, figname):
    from matplotlib import pyplot
    colors = 'bgrcmykw' 
    pyplot.plot(hold=False)  # clear previous plot
    pyplot.hold(True)

    # draw points
    data_colors = [colors[lbl] for lbl in labels]
    pyplot.scatter(X[:, 0], X[:, 1], c=data_colors, alpha=0.5)
    # draw centers
    if centers is not None:
        pyplot.scatter(centers[:, 0], centers[:, 1], s=200, c=colors)
    pyplot.savefig('%s.png' % figname, format='png')
                     
def t_kmeans(X, nclusters):
    centers, labels, inertia = sklearn.cluster.k_means(X, nclusters)
    observer(X, labels, centers, 't_kmeans_%d' % nclusters)
    
def t_gmm(X, nclusters):
    import sklearn.mixture
    
    g = sklearn.mixture.GMM(n_components=3)
    g.fit(X)
    print g.weights_
    centers = g.means_
    labels = g.predict(X)
    observer(X, labels, centers, 't_gmm_%d' % nclusters)
    
def t_spectral(X, nclusters):
    import scipy.spatial
    W = scipy.spatial.distance.cdist(X, X) ** -1
    labels = sklearn.cluster.spectral_clustering(W, nclusters)
    observer(X, labels, None, 't_spectral_%d' % nclusters)
    
def t_dendrogram(X, nclusters):
    from matplotlib.pyplot import show
    from hcluster import pdist, linkage, dendrogram
    import numpy
    from numpy.random import rand
#     X = X[:10, :]
    Y = pdist(X)
    Z = linkage(Y)
    res = dendrogram(Z)
    show()
    pass

if __name__ == '__main__':
    X = loaddata()
    n = 3
#     t_kmeans(X, n)
#     t_gmm(X, n)
#     t_spectral(X, n)
#     from den import do_clustering
#     res = do_clustering(X.tolist())
    t_dendrogram(X, 3)
