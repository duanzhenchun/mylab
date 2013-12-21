from math import *
import numpy as np
import matplotlib.pyplot as plt
path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]
path=np.array(path)

def smooth(path, weight_data = 0.5, weight_smooth = 0.1,tol = 1e-5):
    """
    The update should be done according to the gradient descent equations.
    if to avoid obstables, use max(y_i+1 - y_i)^2 instead of min.
    """
    X = np.array(path, dtype=float)
    Y=X.copy()
    alpha, beta = weight_data, weight_smooth
    assert len(X)==len(Y)
    Yold=np.ones(Y.shape)
    while abs(Yold-Y).sum()>tol:
        Yold=np.copy(Y)
        for i in range(1, len(X)-1):
            Y[i] += alpha*(X[i] - Y[i])
            Y[i] += beta*(Y[i+1] + Y[i-1] - 2* Y[i]) 
    return Y
    
def visual(X,Y):
    for i in range(len(X)):
        print '['+ ', '.join('%.3f'%x for x in X[i]) +'] -> ['+ ', '.join('%.3f'%x for x in Y[i]) +']'
    for A in X,Y:
        plt.plot(A[:,0],A[:,1], 'o-')
    plt.show()
    
newpath = smooth(path)
visual(path, newpath)



