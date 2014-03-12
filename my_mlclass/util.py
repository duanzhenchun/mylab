import numpy as np


STEPS = 100
ALPHA = 0.05

def load_sample(fnames, delimiter=None):
    samples = []
    for fname in fnames:
        f = open(fname)
        samples.append(np.array([[float(j.strip()) for j in i.split(delimiter)] for i in f.readlines()]))
    return samples
    
def addOne(X):
    return np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)
    
def z_scale(X):
    mns = np.mean(X, axis=0)
    sstd = np.std(X, axis=0)
    return (X - mns) / sstd, mns, sstd
    
def sigmoid(z):
    return 1.0 / (1 + np.exp(-z))
 
#derivative of sigmoid
def dsigmoid(z):
    return np.multiply(z, 1-z)

def logist_h(X,theta):
    h= sigmoid(X.dot(theta))
    return h.reshape(h.size,1)
    
def logist_cost(X, y, theta, Lambda=0.0):
    """
    cost function of logistic regression
    """
    h =logist_h(X, theta)
    t1 = y.T.dot(np.log(h)) #np.multiply(y, np.log(h))
    t2 = (1-y).T.dot(np.log(1 - h)) # np.multiply(1 - y, np.log(1 - h))
    cost = t1 + t2
    m = X.shape[0]
    J = -cost.sum() + Lambda * np.linalg.norm(theta[1:]) ** 2 / (2 * m)
    return J.item()


#cost function of linear regression
def linear_cost(X, y, theta, Lambda=0.0):
    delta = X.dot(theta) - y
    J = (delta.T.dot(delta) + Lambda * theta[1:].T.dot(theta[1:])) / (2 * m)
    return J.item()  


def linear_regression(X, y, steps=STEPS, alpha=ALPHA, Lambda=0.0):
    m, n = X.shape
    theta = np.zeros((n, 1))
    Js = []
    alter = np.ones((theta.size,1)); alter[0] = 0 # theta0 should not be regularized
    for _ in range(steps):
        delta = X.dot(theta) - y
        theta = theta *(1 - alpha * Lambda * alter / m) - X.T.dot(delta)* alpha / m
        Js.append(linear_cost(X, y, theta))
    return theta, Js

               
def logistic_regression(X, y0, steps=STEPS, Lambda=0.0):
    """
    using Newton's method
    """
    m, n = X.shape
    y=y0.reshape(y0.size,1)
    theta = np.zeros((n, 1))
    Js = []  
    for _ in range(steps):   
        h = logist_h(X, theta)
        G = theta * (1.*Lambda / m); G[0] = 0  # extra term for gradient
        L = np.eye(n) * (1.*Lambda / m); L[0] = 0  # extra term for Hessian
        grad = X.T.dot(h - y) / m + G
        H = X.T.dot(X) * (np.diag(h) * np.diag(1 - h) / m).item() + L
        theta -= np.linalg.inv(H).dot(grad)
        J = logist_cost(X, y, theta, Lambda)
        Js.append(J)
    return theta, Js
                    
                    
def logistical_min(X, y, Lambda=0.0):
    def costJ(theta, X,y,m, Lambda):
        return logist_cost(X, y, theta,Lambda)
    
    def derivative(theta, X,y,m, Lambda):
        h = logist_h(X, theta)
        G = theta * (float(Lambda) / m); G[0] = 0  # extra term for gradient
        grad = X.T.dot(h-y).flatten() / m + G
        return grad
             
    def hessian(theta, X, Lambda):
        h = logist_h(X, theta)
        L = np.eye(n) * (1.*Lambda / m); L[0] = 0  # extra term for Hessian
        H = X.T.dot(X) * (np.diag(h) * np.diag(1 - h) / m).item() + L
        return H
            
    from scipy import optimize
    m, n = X.shape
    y.shape = y.size,1
    res = optimize.minimize(lambda t: costJ(t, X,y,m, Lambda), np.zeros(n), 
                method='Newton-CG',
                jac=lambda t: derivative(t, X,y,m, Lambda),
                hess=lambda t: hessian(t, X, Lambda),
                options={'disp': True})
    return res

    
def linear_normal_equation(X, y, Lambda=0.0):
    n = X.shape[1]
    theta = np.linalg.inv(X.T.dot(X) + Lambda * np.diag([0] + [1, ] * (n - 1))).dot(X.T).dot(y)
    return theta
    
def polynomial_linear(X, n=6):
    """
    x+x^2+x^3+... => x1,x2,x3,...
    """
    X = np.power(X, range(1, n))
    return addOne(X)

def map_feature(x1, x2, degree=6):
    '''
    Maps the two input features to quadratic features. polynomial terms
 
    Returns a new feature array with more features, comprising of
    X1, X2, X1^2, X2^2, X1*X2, X1*X2^2, etc...

    Inputs X1, X2 must be the same size
    '''
    x1.shape = (x1.size, 1)
    x2.shape = (x2.size, 1)
    x = np.ones(shape=(x1[:, 0].size, 1))
 
    for i in range(1, degree + 1):
        for j in range(i + 1):
            r = (x1 ** (i - j)) * (x2 ** j)
            x = np.append(x, r, axis=1)
    return addOne(x)

def predict_linear(theta, test):
    return np.dot(test, theta).item()
    
def predict_logistic(theta, test, unbias=True):
    """
    prob that class=1.0
    """
    if unbias:
        test = np.append(1, test)
    test.shape = 1, test.size
    return logist_h(test, theta).item()
    
def oneVsAll(X, y):
    """
    k-classification
    """
    steps = 10
    Lambda = X.shape[0]
    kclass = np.unique(y)
    thetas = []
    for k in kclass:
        yk = 1.0 * (y == k)
        theta, _ = logistic_regression(X, yk, steps, Lambda)
        thetas.append(theta)
    return thetas
    
def kclass_predict(test, thetas, unbias=False):
    ys = []
    for theta in thetas:
        y_ = predict_logistic(theta, test, unbias)
        ys.append(y_)
    return np.argmax(ys)

def rand_Eps(m, n, eps):
    return (np.random.rand(m, n) * 2 - 1) * eps

def rand_samples(x):
    """
    random arrange x, so that train and test will not be affected by x's order
    """
    np.random.shuffle(x)
    
def shuffle_data(X, y):
    """
    return new data arrrays
    """
    data = np.append(X, y, axis=1)
    np.random.shuffle(data)
    X, y = np.split(data, (-y.shape[1],), axis=1)
    return X, y

def self_test(X, y, cutratio=0.6):    
    cut = int(X.shape[0] * cutratio)
    X, y = shuffle_data(X, y)
    X, Xtest = np.split(X, (cut,))
    y, ytest = np.split(y, (cut,)) 
    return X, y, Xtest, ytest
    
def calc_contour(data, fn): 
    u = np.linspace(data[:,0].min(), data[:,0].max(), 100)
    v = np.linspace(data[:,1].min(), data[:,1].max(), 100)
    z = np.zeros(shape=(len(u), len(v)))
    for i in xrange(len(u)):
        for j in xrange(len(v)):
            z[i, j] = fn([u[i], v[j]])
    return u,v,z.T
    
