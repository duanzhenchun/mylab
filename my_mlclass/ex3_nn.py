#!/usr/bin/env python

from scipy.io import loadmat
from util import *
import numpy as np


data = loadmat('ex3/ex3data1.mat')
X, y = data['X'], data['y']


def reduceD(X):
    import pca
    from sklearn.preprocessing import scale
    X = scale(X)
    # wired, libPCA is slow in choosing K
    k, Z, Xt = pca.myPCA(X) 
    return Z

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
    #theta0,theta1 = loop(A0,Y,theta0,theta1,Lambda,Steps)
    res = nn_min(X,Y,theta0,theta1,Lambda=1)
    print res.fun
    theta0,theta1=reshape(res.x, A0,Y)
    test(X, y, nnpredict, theta0, theta1)

def reshape(Theta,A0,Y):
    m,n=A0.shape
    t = n + Y.shape[1]
    theta0,theta1=np.vsplit(Theta.reshape(t,Theta.size/t),(n,)) 
    theta0=theta0.T
    return theta0, theta1

def loop(A0,Y,theta0,theta1,Lambda, Steps):
    m,n=A0.shape
    for _ in xrange(Steps):
        A1, A2 = nnforward(A0, theta0, theta1)
        delta2 = A2 - Y  #  5000 * 10  
        delta1 = np.multiply(delta2.dot(theta1), dsigmoid(A1)) # 5000 * 26 
        print _, abs(delta2).sum()
       
        D1 = (delta2.T.dot(A1) + Lambda * theta1) / m  # save as theta1
        D0 = (delta1.T.dot(A0) + Lambda * theta0) / m 
        theta1 -= D1  
        theta0 -= D0 
    return theta0,theta1

def nn_min(X,Y, theta0, theta1, Lambda):
    def costJ(Theta, A0, Y,Lambda):
        m,n=A0.shape
        theta0,theta1 = reshape(Theta, A0, Y)
        A1, A2 = nnforward(A0, theta0, theta1)
        delta2 = A2 - Y  #  5000 * 10  
        delta1 = np.multiply(delta2.dot(theta1), dsigmoid(A1))  # 5000 * 26 
        D1 = (delta2.T.dot(A1) + Lambda * theta1) / m  # save as theta1
        D0 = (delta1.T.dot(A0) + Lambda * theta0) / m 
        J= abs(delta2).sum()
        return J, np.vstack((D0.T, D1)).flatten() 
    
    # merge thetas
    Theta0 = np.vstack((theta0.T, theta1)).flatten()
    from scipy import optimize
    res = optimize.minimize(lambda t: costJ(t,X,Y,Lambda), Theta0, 
                method='CG',
                jac=True, #lambda t: derivative(t,X,Y,Lambda),
                options={'maxiter':100, 'disp': True})
    return res
    
# logistic_predict(X, y)
# given 4000 steps, accuracy reached nearly 100%
neuralnetwork(X, y, 50)
