import numpy as np
import scipy.spatial


A = np.array(
      [[0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0],
       [0, 1, 0, 0, 0, 0],
       [0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 0],
       [0, 0, 0, 0, 1, 0]])

One = np.ones((A.shape[0], 1), dtype=int)
lam = max(np.linalg.eigvals(A))


def Xk(A, k):
    res = One
    for i in range(k):
        res = np.dot(A, res)
    return res

def Xk2(A, k, beta=1.0):
    res = One
    for i in range(k):
        res = np.dot(beta * A.T, res)
    return res

def Ak1(A):
    X = []
    for i in range(1, A.shape[0] + 1):
        X.append(Xk2(A, i, .01))
    return reduce(lambda x1, x2: np.concatenate((x1, x2), axis=1), X)

def calcX(A):
    return np.concatenate((Ak1(A), Ak1(A.T)), axis=1)

def dis(X):
    for i in range(X.shape[0] - 1):
        print scipy.spatial.distance.cosine(X[i], X[i + 1])

