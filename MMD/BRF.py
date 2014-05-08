import numpy as np
from sklearn import cluster

#excercise 7.3.4
k=3
samples=np.array([
    (4,10),(7,10),(4,8),(6,8),(3,4),(10,5),(12,6),(11,4),(2,2),(5,2),(9,3),(12,3),
        ])
res = cluster.k_means(samples, k)
labels=res[1]
clus = [samples[labels==i] for i in range(k)]
print 'cluster i, N, SUM, SUMSQ'
for i in range(k):
    print i, [(clus[i]**j).sum(axis=0) for j in range(3)]
    for j in range(2):
        t=clus[i][:,j]
        print np.var(t), np.std(t)

#density based scan
print cluster.dbscan(samples, eps=3,min_samples=2)
