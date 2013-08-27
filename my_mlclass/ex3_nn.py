#!/usr/bin/env python

from scipy.io import loadmat
from util import *
import numpy as np


data = loadmat('ex3/ex3data1.mat')
X, y = data['X'], data['y']

from pca import *
from sklearn.preprocessing import scale
X = scale(X)
#weired, libPCA is slow in choosing K
#k, Z, Xt = libPCA(X) 
k, Z, Xt = myPCA(X) 
X = addOne(X)

def logistic_predict(X, y):
    thetas = oneVsAll(X, y)
    test(X, y, kclass_predict, thetas,)

    
def test(X, y, func, *args):    
    nright = 0
    ntest = 100    
    for i in np.random.randint(1, len(X), size=ntest):
        prd = func(X[i], *args) + 1
        if prd == y[i]:
            nright += 1
        print prd, y[i]
    print 'accuracy: %.2f' % (1.0 * nright / ntest)

def nnforward(A0, theta0, theta1):
    A1 = sigmoid(A0.dot(theta0.T))  # 5000 * 26 
    A2 = sigmoid(A1.dot(theta1.T))  # 5000 * 10,  h = A2
    return A1, A2

def nnpredict(x, theta0, theta1):
    A1, A2 = nnforward(x, theta0, theta1)
    return np.argmax(A2)

def neuralnetwork(X, y, Steps=400, Lambda=0.01):
    # Layers = 3
    m, n = X.shape
    s0 = n
    s1 = 25 + 1
    s2 = np.unique(y).size
    
    # transpose y to matrix
    Y = np.zeros((y.size, s2))  # 5000 * 10
    for i in xrange(y.size):
        Y[i, y[i][0] - 1] = 1.0 
    
    epsilon = 6 ** .5 / (n ** .5 + s2 ** .5)
    theta0 = rand_Eps(s1, s0, epsilon)  # 26 * 401
    theta1 = rand_Eps(s2, s1, epsilon)  # 10 *  26    
        
    A0 = X  # 5000,401
    
    for _ in xrange(Steps):
        A1, A2 = nnforward(A0, theta0, theta1)
        delta2 = A2 - Y  #  5000 * 10  
        delta1 = np.multiply(delta2.dot(theta1), np.multiply(A1, 1.0 - A1))  # 5000 * 26 
    
        print _, abs(delta2).sum()
        
        D1 = (delta2.T.dot(A1) + Lambda * theta1) / m  # save as theta1
        D0 = (delta1.T.dot(A0) + Lambda * theta0) / m 
        theta1 -= D1  
        theta0 -= D0 
    test(X, y, nnpredict, theta0, theta1)

# logistic_predict(X, y)
# given 4000 steps, accuracy reached nearly 100%
neuralnetwork(X, y, 400)
