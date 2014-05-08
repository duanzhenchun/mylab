# algrithm by Mining Massive Data, 9.4.5

import numpy as np
from cf_mf import RMSE

def CF():
    U,V,norm = optimize(M)
    return U.dot(V)+norm

def init(R, K, sigma = 0.1):
    N,M = R.shape
    a = R.sum()/(R!=0).sum()
    print a, K
    t = (a/K)**0.5
    U = t*(1 + np.random.randn(N,K)*sigma)
    V = t*(1 + np.random.randn(K,M)*sigma)
    return U,V

def optimize(M, Iter=100):
    norm = np.average(M, axis=1, weights=(M!=0)) 
    M1 = M - norm
    U,V = init(M, d)
    for i in xrange(Iter):
        improve(U, V, M, M1)
        if not i%10:
            P = U.dot(V)+norm
            print i, RMSE(P,M)
    return U,V, norm

def improve(U, V, M, M1):
    for r in xrange(n):
        for s in xrange(d):
            if M[r,s]==0: continue
            All, denom = 0.0, 0.0
            for j in xrange(m):
                t = M1[r,j]
                for k in xrange(d):
                    if k == s:
                        continue
                    t -= U[r,k] * V[k,j]
                All += V[s,j]*t
                denom += V[s,j]**2
            U[r,s] = All/denom

    for r in xrange(d):
        for s in xrange(m):
            if M[r,s]==0: continue
            All, denom =0.0, 0.0
            for i in xrange(n):
                t=M1[i,s]
                for k in xrange(d):
                    if k == r: 
                        continue
                    t -= U[i,k] * V[k,s]
                All += U[i,r]*t
                denom += U[i,r]**2
            V[r,s ] = All/denom

example_99 = [  #users * items
        [5,2,4,4,3],
        [3,1,2,4,1],
        [2,0,3,1,4],
        [2,5,4,3,5],
        [4,4,5,4,0],]

M = np.array(example_99, dtype=float)
n, m = M.shape
d = 2
P = CF()
print P


