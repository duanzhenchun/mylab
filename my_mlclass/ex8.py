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

if __name__ == '__main__':
#    anomaly()
#    show_threshold()
    show_threshold('ex8/ex8data2.mat')
