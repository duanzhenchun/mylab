from numpy import *

STEPS = 100
ALPHA = 0.05

def load_sample(fnames, delimiter=' '):
    samples = []
    for fname in fnames:
        f = open(fname)
        samples.append(array([[float(j.strip()) for j in i.split(delimiter)] for i in f.readlines()]))
    return samples
    
    
def z_scale(x):
    mns = mean(x,axis=0)
    sstd = std(x,axis=0)
    return (x - mns) / sstd, mns, sstd
    
def sigmoid(z):
    return 1.0 / (1.0 + exp(-z))

def J_logistic(y,h):
    """
    cost function of logistic
    """
    t1 = multiply(y, log(h))
    t2 = multiply(1-y, log(1-h))
    cost = t1+t2
    return -sum(cost)/cost.size

def linear_regression( x, y, steps=STEPS, alpha=ALPHA, Lambda=0.0 ):
    m,n = x.shape
    theta=zeros((n,1))
    Js=[] 
    for i in range(steps):   
        delta = x * theta - y
        theta = theta * (1 - alpha * Lambda / m) - (delta.T * x * alpha / m).T
        J = (linalg.norm(delta) + linalg.norm(theta[1:])*Lambda) /(2*m)
        Js.append(J)
    return theta, Js
                
def logistic_regression(x,y, steps=STEPS, Lambda = 0.0):
    """
    using Newton's method
    """
    m,n =x.shape
    theta = zeros((n,1))
    Js=[]  
    for i in range(steps):   
        z = x*theta
        h = sigmoid(z)
        G = theta * (1.*Lambda / m); G[0] = 0  # extra term for gradient
        L = eye(n) * (1.*Lambda / m); L[0] = 0  # extra term for Hessian
        grad = x.T * (h - y) / m + G
        H = x.T * x * (diag(h) * diag(1 - h) / m).item() + L
        theta -= linalg.inv(H) * grad
        Js.append(J_logistic(y, h) + Lambda / (2 * m) * linalg.norm(theta[1:]))
    return theta, Js

    
def linear_normal_equation(x,y, Lambda = 0.0):
    n=x.shape[1]
    theta = linalg.inv(x.T * x + Lambda * diag([0]+[1,]*(n-1))) * x.T * y
    return theta
    
def polynomial_linear(x, n=6):
    """
    x+x^2+x^3+... => x1,x2,x3,...
    """
    x = power(x,range(1,n))
    return mat(concatenate((ones((x.shape[0],1)),x),axis=1))

def map_feature(x1, x2, degree=6):
    '''
    Maps the two input features to quadratic features. polynomial terms
 
    Returns a new feature array with more features, comprising of
    X1, X2, X1^2, X2^2, X1*X2, X1*X2^2, etc...

    Inputs X1, X2 must be the same size
    '''
    x1.shape = (x1.size, 1)
    x2.shape = (x2.size, 1)
    out = ones(shape=(x1[:, 0].size, 1))
 
    for i in range(1, degree + 1):
        for j in range(i + 1):
            r = (x1 ** (i - j)) * (x2 ** j)
            out = append(out, r, axis=1)
        
    x = out
    return mat(concatenate((ones((x.shape[0], 1)), x), axis=1))


