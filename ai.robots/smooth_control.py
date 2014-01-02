from math import *
from utils import *


def smooth( path, weight_data = 0.5, weight_smooth = 0.1,
            fixed=[], circular=False, tol = 1e-5):
    """
    Use descent equations.
    if to avoid obstables, use max(y_i+1 - y_i)^2 instead of min.
    """
    X = np.array(path, dtype=float)
    Y=X.copy()
    alpha, beta = weight_data, weight_smooth
    assert len(X)==len(Y)
    N=len(X)
    Yold=np.ones(Y.shape)
    Xrange=circular and (0,N) or(1,N-1)
    while abs(Yold-Y).sum()>tol:
        Yold=np.copy(Y)
        for i in range(*Xrange):
            if i in fixed:
                continue
            Y[i] += alpha*(X[i] - Y[i])
            if circular or 0<i<N-1:
                Y[i]+=beta*(Y[(i-1)%N] + Y[(i+1)%N] -(2*Y[i]))
            if circular or i>=2:
                Y[i] += 0.5*beta*(2*Y[(i-1)%N] - Y[(i-2)%N] - Y[i%N]) 
            if circular or i<N-2:
                Y[i] += 0.5*beta*(2*Y[(i+1)%N] - Y[(i+2)%N] - Y[i%N])
    return Y
    


def test_smooth():
    path=[[0, 0], 
      [1, 0],
      [2, 0],
      [3, 0],
      [4, 0],
      [5, 0],
      [6, 0],
      [6, 1],
      [6, 2],
      [6, 3],
      [5, 3],
      [4, 3],
      [3, 3],
      [2, 3],
      [1, 3],
      [0, 3],
      [0, 2],
      [0, 1]]
    newpath = smooth(path, 0.5, 0.1, circular=True)#, fixed=(0,6,9,15))
    visual2D(path, newpath)


if __name__ == '__main__':  
    test_smooth()
