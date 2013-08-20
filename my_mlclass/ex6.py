from util import *
import numpy as np

def cost_svm(F, y, theta, C):
    z = F * theta
    Zeros = zeros((z.size,1))
    
    cost1 = np.max(append(Zeros, 1-z, axis=1), axis=1)  # max(0, 1-z), hinge loss# max(0, 1-z), hinge loss
    cost0 = np.max(append(Zeros, 1+z, axis=1), axis=1)  
    cost = multiply(y, cost1) + multiply(1-y, cost0)
    J = sum(cost) *C  + 0.5 * linalg.norm(theta[1:])**2
    return J
    
def gaussian(x, mu, sigma):
    return exp(-linalg.norm(x-mu)**2/(2*sigma**2))
    
def lin_kernel(x,l):
    return multiply(x,l)
        
def kernel(X, sim=gaussian, sigma=2.0):
    m = X.shape[0]
    F=zeros((m,m))
    for i in range(m):
        F[i]=apply_along_axis(lambda x:gaussian(x,X[i],sigma),1,X)
    return mat(F)    # m*m

X=array(range(6))
X.shape=3,2
X=addOne(X) 
y=array([1,0,1])
y.shape=3,1
C=1
theta = ones((X.shape[0],1))*.5
F= kernel(X)
cost_svm(F,y, theta, C)

