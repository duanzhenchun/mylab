#!/usr/bin/env python

import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn.covariance import EmpiricalCovariance, MinCovDet
from sklearn.metrics import fbeta_score
from sklearn.decomposition import PCA
import scipy
from util import *


def gaussian_prod(x, mean, std):
    res=scipy.stats.norm.pdf(x,loc=mean,scale=std)
    return res.prod()
    
def anplot(data, fn, use_exps=True):
    xs, ys, z = calc_contour(data, fn)

    plt.scatter(data[:,0], data[:,1], marker='x')
    if use_exps:
        exps = np.arange(-20, -1, 3)
        fn = np.vectorize(lambda n: 10**n)
        plt.contour(xs, ys, z, fn(exps))
    else:
        plt.contour(xs, ys, z)
    plt.grid()
    plt.show()


def anomaly():
    raw = loadmat('ex8/ex8data1.mat')
    X = raw['X']
    
    # independent variables
    anplot(X, lambda x: gaussian_prod(x, X.mean(0), X.std(0)))

    # cov-variable Gaussian
#    cov = EmpiricalCovariance().fit(X)
    cov = MinCovDet().fit(X)
    anplot(X, cov.score, False)


def find_threshold(fn,Xcv,ycv):
    """
    by cv testing on (Xval,yval)
    """
    dists = np.fromiter((fn(x) for x in Xcv), float)
    best = (0,0)    #threshold, f1_score
    print dists.min(), dists.max()
##    for t in dists:    # for each prob score
    for t in np.linspace(dists.min(), dists.max(), 100):
        preds = (dists < t).astype(int)
        f = fbeta_score(ycv, preds, 1.)
        if f > best[1]:
            best = (t,f)
    return best


def predict_anomal(fn, X, t):
    res = []
    for x in X:
        if fn(x) < t:
            res.append(x)
    return np.array(res)
    
    
def show_threshold(fname='ex8/ex8data1.mat'):
    raw = loadmat(fname)
    X = raw['X']
    Xcv = raw['Xval']
    ycv = raw['yval'].ravel()
    cov = EmpiricalCovariance().fit(X)
#    cov = MinCovDet().fit(X)
    print cov.location_, cov.covariance_
    t, f = find_threshold(cov.score, Xcv, ycv)
    print('threshold: {}\nfscore: {}'.format(t, f))
    reds = predict_anomal(cov.score, X, t)
    print 'abnorma num:', reds.shape[0]
    
    if X.shape[1]>2:
        pca = PCA(2)
        X = pca.fit_transform(X)
        print pca.explained_variance_ratio_     # about 0.5, 2D is not enough to compress X
        reds = pca.transform(reds)
    else:        
        xs, ys, z = calc_contour(X, cov.score)
        plt.contour(xs, ys, z)

    plt.scatter(X[:,0], X[:,1], marker='x')
    plt.scatter(reds[:,0], reds[:,1], marker='o', color='red')
    plt.grid()
    plt.show()

def movie_recommend(fname='ex8/ex8_movies.mat', n=100):
    raw = loadmat(fname)
    Y,R=raw['Y'], raw['R']
    Lambda = 1
    MIter = 100
    
#     nm,nu,n=500,400,30
#     Y = Y[:nm,:nu]
#     R = R[:nm,:nu]
    
    nm,nu=Y.shape
#     use_fmin(R,Y,Lambda)
    idx = (R==1)  
    X=np.ones((nm,n))/n/nm
    Theta = np.ones((nu,n))/n/nu
    Js=[]
    for i in xrange(MIter):
#         Xgrad = numgradient(X, lambda x: costJ(x,Theta,R,Y,Lambda))
#         Thetagrad = numgradient(Theta, lambda theta: costJ(X,theta,R,Y,Lambda))
        Xgrad, Thetagrad = gradient(X, Theta, idx, Y, Lambda)
        alpha = 1.0/(i+500)
        X -= alpha * Xgrad
        Theta -= alpha * Thetagrad
        J = costJ(X, Theta, R, Y, Lambda)
        print i,alpha, J
        Js.append(J)
    return X,Theta,Js
    
def small_test(Y,R):
    nm,nu,n=5,4,3
    X=np.array([1.048686,-0.400232, 1.194119, 0.780851,-0.385626, 0.521198, 0.641509,-0.547854,-0.083796, 0.453618,-0.800218, 0.680481, 0.937538, 0.106090, 0.361953])
    Theta=np.array([ 0.28544,  -1.68427,0.26294,0.50501,  -0.45465,0.31746,  -0.43192 , -0.47880,0.84671,0.72860,  -0.27189,0.32684])
    X.shape=nm,n
    Theta.shape=nu,n
    Y = Y[:nm,:nu]
    R = R[:nm,:nu]

def gradient(X, Theta, idx, Y, Lambda):
    nm,nu=Y.shape
    n=X.shape[1]
    Xgrad = np.zeros((nm,n))
    Thetagrad = np.zeros((nu,n))
    nm,nu=Y.shape
    # matrix not fit here
#    Xgrad=np.dot((np.dot(X,Theta.T) - Y), Theta)
#    Thetagrad=np.dot((np.dot(X,Theta.T) - Y).T, X)
    for i in xrange(nm):
        Theta_tmp = Theta[idx[i],:] # t x n
        Y_tmp = Y[i,idx[i]]        # 1 x t
        delta = np.dot(X[i,:], Theta_tmp.T) - Y_tmp             # 1 x t
        Xgrad[i] = np.dot(delta, Theta_tmp) + Lambda * X[i,:]   # 1 x n
    for j in xrange(nu):
        X_tmp = X[idx[:,j],:]       # t x n
        Y_tmp = Y[idx[:,j],j]       # t x 1
        delta = np.dot(X_tmp, Theta[j,:].T) - Y_tmp                 # t x 1
        Thetagrad[j] = np.dot(delta.T, X_tmp) + Lambda * Theta[j,:] # 1 x n
    return [Xgrad, Thetagrad]
    
def numgradient(X, J):
    """
    Computes the gradient using "finite differences"
    and gives us a numerical estimate of the gradient.
    """
    perturb = np.zeros(X.shape)
    grad = np.zeros(X.shape)
    e = 1e-4
    for i, _ in np.ndenumerate(X):
        # Set perturbation vector
        perturb[i] = e
        loss1 = J(X - perturb)
        loss2 = J(X + perturb)
        # Compute Numerical Gradient
        grad[i] = (loss2 - loss1) / (2*e)
        perturb[i] = 0
    return grad
    
def costJ(X, Theta, R, Y, Lambda):
    return (((np.dot(X, Theta.T) - Y) * R)**2).sum() /2 + Lambda/2*((X**2).sum() + (Theta**2).sum())


def use_fmin(R,Y,Lambda):
    def f(Xs, *args):
        [X,Theta] = Xs
        R,Y,Lambda = args
        return costJ(X,Theta, R, Y, Lambda)

    def gradf(Xs, *args):
        [X,Theta] = Xs
        R,Y,Lambda = args        
        idx = (R==1)
        return gradient(X, Theta, idx, Y, Lambda)
    from scipy import optimize
    args = (R,Y,Lambda)
    nm,nu=Y.shape
    n=100
    X0=np.ones((nm,n))/n/nm
    Theta0 = np.ones((nu,n))/n/nu
    res = optimize.fmin_cg(f, [X0,Theta0], fprime=gradf, args=args)
    print res
    return res
    

if __name__ == '__main__':
#    anomaly()
#    show_threshold()
#    show_threshold('ex8/ex8data2.mat')
    movie_recommend()
