import numpy as np
import pylab as pl
from sklearn import mixture


n_samples = 300
c_types = ['full', 'diag', 'spherical']
np.random.seed(0)
C = np.array([[0., -0.7], [3.5, 1.7]])
X_train = np.dot(np.random.randn(n_samples, 2), C)

pl.figure(dpi=100, figsize=(3, 3))
pl.scatter(X_train[:, 0], X_train[:, 1], .8)
pl.axis('tight')
pl.savefig('GaussianFit-data.svg')
pl.close()
for c_type in c_types:
    clf = mixture.GMM(n_components=1, covariance_type=c_type)
    clf.fit(X_train)
    x = np.linspace(-15.0, 20.0, num=200)
    y = np.linspace(-10.0, 10.0, num=200)
    X, Y = np.meshgrid(x, y)
    XX = np.c_[X.ravel(), Y.ravel()]  # flatten
    Z = np.log(-clf.eval(XX)[0])
    Z = Z.reshape(X.shape)
    
    pl.figure(dpi=100, figsize=(3, 3))
    CS = pl.contour(X, Y, Z)
    pl.scatter(X_train[:, 0], X_train[:, 1], .8)
    pl.axis('tight')
    pl.savefig('GaussianFit-%s.svg' % c_type)
    pl.close()
