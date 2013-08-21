from sklearn.decomposition import PCA
import numpy as np

def libPCA(X, precison=0.95):
    m,n = X.shape
    for k in range(1, n):
        pca = PCA(k)
        Z = pca.fit_transform(X)
        print 'k: %s, precison: %s' %(k, pca.explained_variance_ratio_[0])
        if pca.explained_variance_ratio_[0] > precison:
            break
    Xinv = pca.inverse_transform(Z)
    return k, Z, Xinv

def myPCA(X, precison=0.95):
    m,n = X.shape
    Sigma = np.dot(X.T, X) /m
    U,S,V = np.linalg.svd(Sigma)
    for k in range(1, n):
        p = S[:k].sum()/S.sum()
        print 'k: %s, precison: %s' %(k, p)
        if p > precison:
            break
    Ur=U[:,:k]
    Z = np.dot(X, Ur)
    Xinv = np.dot(Z, Ur.T)
    return k, Z, Xinv
