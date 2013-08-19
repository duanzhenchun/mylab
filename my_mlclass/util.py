from numpy import *

STEPS = 100
ALPHA = 0.05

def load_sample(fnames, delimiter=None):
    samples = []
    for fname in fnames:
        f = open(fname)
        samples.append(array([[float(j.strip()) for j in i.split(delimiter)] for i in f.readlines()]))
    return samples
    
    
def z_scale(x):
    mns = mean(x, axis=0)
    sstd = std(x, axis=0)
    return (x - mns) / sstd, mns, sstd
    
def sigmoid(z):
    return 1.0 / (1 + exp(-z))


def cost_logistic(y, h):
    """
    cost function of logistic
    """
    t1 = multiply(y, log(h))
    t2 = multiply(1 - y, log(1 - h))
    cost = t1 + t2
    return -sum(cost) / cost.size

def linear_regression(x, y, steps=STEPS, alpha=ALPHA, Lambda=0.0):
    m, n = x.shape
    theta = zeros((n, 1))
    Js = [] 
    for i in range(steps):   
        delta = x * theta - y
        theta = theta * (1 - alpha * Lambda / m) - (delta.T * x * alpha / m).T
        J = (linalg.norm(delta) + linalg.norm(theta[1:]) * Lambda) / (2 * m)
        Js.append(J)
    return theta, Js
                
def logistic_regression(x, y, steps=STEPS, Lambda=0.0):
    """
    using Newton's method
    """
    m, n = x.shape
    theta = zeros((n, 1))
    Js = []  
    for i in range(steps):   
        z = x * theta
        h = sigmoid(z)
        G = theta * (1.*Lambda / m); G[0] = 0  # extra term for gradient
        L = eye(n) * (1.*Lambda / m); L[0] = 0  # extra term for Hessian
        grad = x.T * (h - y) / m + G
        H = x.T * x * (diag(h) * diag(1 - h) / m).item() + L
        theta -= linalg.inv(H) * grad
        J = cost_logistic(y, h) + Lambda / (2 * m) * linalg.norm(theta[1:])
        print J
        Js.append(J)
    return theta, Js
                    
def logis_fmin(x, y):
    def f(x, *args):
        y, h, m = args
        return cost_logistic(y, h)
    def gradf(x, *args):
        y, h, m = args
        x.shape = m, x.size / m
        grad = x.T * (h - y) / m 
        return grad    
    from scipy import optimize
    m, n = x.shape
    theta = zeros((n, 1))
    z = x * theta
    h = sigmoid(z)
    args = (y, h, m)
    res = optimize.fmin_cg(f, x, fprime=gradf, args=args)
    print res
    
def linear_normal_equation(x, y, Lambda=0.0):
    n = x.shape[1]
    theta = linalg.inv(x.T * x + Lambda * diag([0] + [1, ] * (n - 1))) * x.T * y
    return theta
    
def polynomial_linear(x, n=6):
    """
    x+x^2+x^3+... => x1,x2,x3,...
    """
    x = power(x, range(1, n))
    return mat(concatenate((ones((x.shape[0], 1)), x), axis=1))

def map_feature(x1, x2, degree=6):
    '''
    Maps the two input features to quadratic features. polynomial terms
 
    Returns a new feature array with more features, comprising of
    X1, X2, X1^2, X2^2, X1*X2, X1*X2^2, etc...

    Inputs X1, X2 must be the same size
    '''
    x1.shape = (x1.size, 1)
    x2.shape = (x2.size, 1)
    x = ones(shape=(x1[:, 0].size, 1))
 
    for i in range(1, degree + 1):
        for j in range(i + 1):
            r = (x1 ** (i - j)) * (x2 ** j)
            x = append(x, r, axis=1)
    x = mat(concatenate((ones((x.shape[0], 1)), x), axis=1))
    return x
    

def predict_linear(theta, test):
    return dot(test, theta).item()
    
def predict_logistic(theta, test, unbias=True):
    """
    prob that class=1.0
    """
    if unbias:
        test = append(1, test)
    test.shape = 1, test.size
    return sigmoid(dot(test, theta)).item()
    
def oneVsAll(x, y):
    """
    k-classification
    """
    steps = 10
    Lambda = x.shape[0]
    kclass = unique(y)
    thetas = []
    for k in kclass:
        yk = 1.0 * (y == k)
        theta, Js = logistic_regression(x, yk, steps, Lambda)
        thetas.append(theta)
    return thetas
    
def kclass_predict(test, thetas, unbias=False):
    ys = []
    for theta in thetas:
        y_ = predict_logistic(theta, test, unbias)
        ys.append(y_)
    return argmax(ys)

def rand_Eps(m, n, eps):
    return (random.rand(m, n) * 2 - 1) * eps
