from math import *
import numpy as np
import matplotlib.pyplot as plt

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
path=np.array(path)
fixed=(0,6,9,15)

def smooth(path, weight_data = 0.5, weight_smooth = 0.1,tol = 1e-5):
    """
    The update should be done according to the gradient descent equations.
    if to avoid obstables, use max(y_i+1 - y_i)^2 instead of min.
    """
    X = np.array(path, dtype=float)
    Y=X.copy()
    alpha, beta = weight_data, weight_smooth
    assert len(X)==len(Y)
    N=len(X)
    Yold=np.ones(Y.shape)
    while abs(Yold-Y).sum()>tol:
        Yold=np.copy(Y)
        for i in range(N):
            if i in fixed:
                continue
            #circulic smoothing
            Y[i] += alpha*(X[i] - Y[i])
            Y[i] -= 0.5*beta*(Y[(i-2)%N] + Y[i%N] - 2*Y[(i-1)%N]) 
            Y[i] -= 0.5*beta*(Y[(i+2)%N] + Y[i%N] - 2*Y[(i+1)%N])
    return Y
    
def visual(X,Y):
    for i in range(len(X)):
        print '['+ ', '.join('%.3f'%x for x in X[i]) +'] -> ['+ ', '.join('%.3f'%x for x in Y[i]) +']'
    for A in X,Y:
        plt.plot(A[:,0],A[:,1], 'o-')
    plt.show()
    
newpath = smooth(path, 0.5, 0.1)
visual(path, newpath)
