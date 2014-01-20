import math
import numpy as np


lambdaU=lambdaV=0.02
lambdaT=1.0


def sigmoid(z):
    return z
    return 1.0 / (1 + np.exp(-z))

def dsigmoid(z):
    return 1.0
    return np.exp(-z)/(1+np.exp(-z))**2

def costL(R,T,U,V):
    N,M=R.shape
    cost=0.0
    for u in xrange(N):
        for i in xrange(M):
            if R[u][i]>0:
                cost += (R[u][i]-sigmoid(U[u].dot(V[:,i].T)))**2
    cost += lambdaU/2*np.linalg.norm(U)+lambdaV/2*np.linalg.norm(V)
    for u in xrange(N):
        e = U[u] - T[u].dot(U) #1xK
        cost += lambdaT/2*e.dot(e.T)
    return cost

def partial(R,T,U,V):
    dU = np.zeros(U.shape)
    dV = np.zeros(V.shape)
    N,M=R.shape
    for u in xrange(N):
        for i in xrange(M):
            if R[u][i] >0:
                tmp = U[u].dot(V[:,i].T)
                dU[u] += V[:,i].dot(dsigmoid(tmp)*(tmp-R[u][i])) 
        dU[u] += lambdaU * U[u]
        tmp = 0.0
        for v in xrange(N):
            if T[v][u]>0:
                tmp += T[v][u]*(U[v] - T[v].dot(U))
        dU[u] +=lambdaT * (U[u] - T[u].dot(U) - tmp)

    for i in xrange(M):
        for u in xrange(N):
            if R[u][i]>0:
                tmp = U[u].dot(V[:,i].T)
                dV[:,i] += U[u].dot(dsigmoid(tmp)*(tmp-R[u][i]))
    dV[:,i] += lambdaV * V[:,i]
    return dU,dV

def init(S0,N):
    S=np.zeros((N,N))
    for u,vs in enumerate(S0):
        for v in vs:
            S[u][v-1]=1
    return S
 
def socialMF(R, T, K, steps=10**3, alpha=0.002, tol=1e-5):
    N,M=R.shape
    U = np.random.rand(N,K)
    V = np.random.rand(K,M)
    for step in xrange(steps):
        dU,dV = partial(R,T,U,V)
        U -= alpha * dU
        V -= alpha * dV
        e = costL(R,T,U,V)
        print e
        if e < tol:
            break
    print 'step:%d, e: %f' %(step, e)
    return U, V


if __name__ == "__main__":
    R = [
         [5,3,0,1],
         [4,0,0,1],
         [1,1,0,5],
         [1,0,0,4],
         [0,1,5,4],
        ]
    R=np.array(R)
    T = [[3,5],[1,3,4],[2],[1,5],[3]]
    T = init(T, R.shape[0])
    U,V = socialMF(R,T,K=2)
    print 'R_hat:\n', U.dot(V)

