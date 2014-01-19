#!/usr/bin/python
#
# Created by Albert Au Yeung (2010)
#
# An implementation of matrix factorization
#
import numpy

###############################################################################

"""
@INPUT:
    R     : a matrix to be factorized, dimension N x M
    P     : an initial matrix of dimension N x K
    Q     : an initial matrix of dimension M x K
    K     : the number of latent features
    steps : the maximum number of steps to perform the optimisation
    alpha : the learning rate
    beta  : the regularization parameter
@OUTPUT:
    the final matrices P and Q
"""
def matrix_factorization(R, K, steps=5000, alpha=0.0002, beta=0.02, tol=1e-3):
    N,M=R.shape
    P = numpy.random.rand(N,K)
    Q = numpy.random.rand(M,K)
    Q = Q.T
    for step in xrange(steps):
        for i in xrange(N):
            for j in xrange(M):
                if R[i][j] > 0:
                    eij = R[i][j] - P[i,:].dot(Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        #R_hat = P.dot(Q)
        #error with regularization
        e = 0
        for i in xrange(N):
            for j in xrange(M):
                if R[i][j] > 0:
                    e += (R[i][j] - P[i,:].dot(Q[:,j]))**2
                    for k in xrange(K):
                        e += beta/2 * ( P[i][k]**2 + Q[k][j]**2)
        if e < tol:
            break
    print step
    return P, Q.T

###############################################################################

if __name__ == "__main__":
    R = [
         [5,3,0,1],
         [4,0,0,1],
         [1,1,0,5],
         [1,0,0,4],
         [0,1,5,4],
        ]
    R = numpy.array(R)
    K = 2
    P, Q = matrix_factorization(R, K)
    print P.dot(Q.T)
