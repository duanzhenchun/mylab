#!/usr/bin/env python

from scipy.io import loadmat
from sklearn.decomposition import PCA
from scipy import optimize
from util import *
    
def loadMovieList():
    lst=[]
    with open('ex8/movie_ids.txt') as f:
        for l in f.readlines():
            n, name = l.split(' ',1)
            lst.append(name.strip())
    return lst

def meanY(Y,idx):
    nm,n=Y.shape
    Ymean = np.zeros(nm)
    for i in range(nm):
        Ymean[i]=Y[i,idx[i]].mean()
    return Ymean
 
def recommend(Ymean): 
    nm = Ymean.size
    mine = Ymean.reshape(nm,1)
    for i,j in [(1,4),(98,2),(7,3),(12,5),(54,4),(64,5),(66,3),(69,5),(183,4),(226,5),(355,5)]:
        mine[i-1] = j
    return mine
     
def movie_recommend(fname, n, MIter, Lambda):
    print n,MIter,Lambda
    raw = loadmat(fname)
    Y,R=raw['Y'], raw['R']

    # make small area
#     nm,nu,n=500,400,30
#     Y = Y[:nm,:nu]
#     R = R[:nm,:nu]

    nm,nu=Y.shape
    idx = (R==1)  
    Ymean=meanY(Y,idx)
    
#     X,Theta,Js = loop(Y,R, n, MIter, Lambda)

    res = use_fmin(R,Y,n, Lambda, MIter)
    print res.fun
    X,Theta = reshape(res.x,nm,n)
    
    p = X.dot(Theta.T)
    print 'err:  ', ((Y[idx]-p[idx])**2).sum()
    predict = recommend(Ymean)
    
    movieList = loadMovieList()
    ix = sorted(enumerate(predict),key=lambda x:x[1],reverse=True)
    print 'Top recommendations for you:'
    for i in range(10):
        j = ix[i][0]
        print 'Predicting rating %.1f for movie %s' %(predict[j], movieList[j])
    
    
def loop(Y,R, n, MIter, Lambda):
    nm,nu=Y.shape
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
    return Xgrad, Thetagrad
    
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
    return (((X.dot(Theta.T) - Y) * R)**2).sum() /2 + Lambda/2*((X**2).sum() + (Theta**2).sum())

def reshape(Xs,nm,n):
    X,Theta=np.vsplit(Xs.reshape(Xs.size/n,n),(nm,)) 
    return X, Theta

def use_fmin(R,Y,n,Lambda, MIter):
    def cost(Xs, R,Y,n,Lambda):
        nm,nu=Y.shape
        X,Theta = reshape(Xs,nm,n)
        J= costJ(X,Theta, R, Y, Lambda)
        print J
        idx = (R==1)
        Xgrad, Thetagrad = gradient(X, Theta, idx, Y, Lambda)
        return J, np.vstack((Xgrad, Thetagrad)).flatten()
    
    nm,nu=Y.shape
    X0 = rand_Eps(nm,n, 1.0/n) 
    Theta0 = rand_Eps(nu,n,1.0/n) 
    res = optimize.minimize(lambda t: cost(t,R,Y,n,Lambda), 
                np.vstack((X0, Theta0)).flatten(), 
                method='CG',
                jac=True, #lambda t: derivative(t,X,Y,Lambda),
                options={'maxiter':MIter, 'disp': True})
    return res

    
def small_test(Y,R):
    nm,nu,n=5,4,3
    X=np.array([1.048686,-0.400232, 1.194119, 0.780851,-0.385626, 0.521198, 0.641509,-0.547854,-0.083796, 0.453618,-0.800218, 0.680481, 0.937538, 0.106090, 0.361953])
    Theta=np.array([ 0.28544,  -1.68427,0.26294,0.50501,  -0.45465,0.31746,  -0.43192 , -0.47880,0.84671,0.72860,  -0.27189,0.32684])
    X.shape=nm,n
    Theta.shape=nu,n
    Y = Y[:nm,:nu]
    R = R[:nm,:nu]
    
if __name__ == '__main__':
    import sys
    MIter,Lambda = 100,1
    if len(sys.argv)>2:
        MIter, Lambda = sys.argv[1:3]
    movie_recommend('ex8/ex8_movies.mat',100, int(MIter), float(Lambda))
