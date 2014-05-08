#!/usr/bin/python
# modified from 
#http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python/

import numpy as np

def CF(R, K, max_steps=5000, 
        alpha=0.2, beta=0.2, tol=1e-3):
    """
    @INPUT:
        R     : a matrix to be factorized, dimension N x M, R = UV
                empty if R[i,j] == 0
        K     : the number of latent features
        alpha : the learning rate
        beta  : the regularization parameter
    @OUTPUT:
        the final matrices U[N x K] and V[K x M]
    """
    def optimize():
        for i in xrange(N):
            for j in xrange(M):
                if R[i][j] > 0:
                    eij = R[i][j] - U[i,:].dot(V[:,j])
                    for k in xrange(K):
                        U[i][k] += alpha * (2 * eij * V[k][j] - beta * U[i][k])
                        V[k][j] += alpha * (2 * eij * U[i][k] - beta * V[k][j])

    def costf():
        e = 0
        for i in xrange(N):
            for j in xrange(M):
                if R[i][j] > 0:
                    e += (R[i][j] - U[i,:].dot(V[:,j]))**2
        e += beta/2*(np.linalg.norm(U)+np.linalg.norm(V))
        return e

    N,M=R.shape
    U, V = init(R,K)
    alpha /=(N*M)
    stage = max(max_steps/100 , 1)
    min_steps = min(stage, 100)
    for step in xrange(max_steps):
        optimize()
        if not step%stage:
            e = costf()
            #print 'step: %d, e: %f' %(step, e)
            if e < tol and step>min_steps:
                break
    return U, V

def normalize(R):
    N,M = R.shape
    I=(R!=0)*1.0
    norm0 = np.average(R, axis=0, weights=I) 
    norm1 = np.average(R, axis=1, weights=I)
    norm = (I*norm0.reshape(1,M) + I*norm1.reshape(N,1))*0.5
    return norm

def init(R, K):
    N,M = R.shape
    sigma = np.std(R) **0.5
    U = np.random.randn(N,K)*sigma
    V = np.random.randn(K,M)*sigma
    return U,V

def RMSE(R_hat, R):
    a = ((R_hat*(R!=0)-R)**2).sum()
    c = (R!=0).sum()
    return (a/c)**0.5

if __name__ == "__main__":
    R = np.array([
         [5,3,0,1],
         [4,0,0,1],
         [1,1,0,5],
         [1,0,0,4],
         [0,1,5,4],
        ], dtype=float)
    K = 2
    ave = 0.0
    repeats = 1
    for i in range(repeats):
        U, V = CF(R, K, max_steps=10**3)
        R_hat = U.dot(V)
        print 'R:\n', R
        print 'R_hat\n:', R_hat
        e = RMSE(R_hat, R)
        print 'RMSE:', e 
        ave += e
    print 'ave:', ave/repeats

