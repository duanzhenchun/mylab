from ex6_3 import *
from util import *


def svm_best(X,y, **kw):
    params = (0.01,0.03, 0.1,0.3, 1,3, 10,30)

    cut=int(X.shape[0] * 0.6)
    Xtrain, Xtest = np.split(X,(cut,))
    ytrain, ytest = np.split(y,(cut,))
            
    results=[]
    for C in params:
        for gamma in params:  # gamma= 1 / sigma
            clf=svm.SVC(C=C,gamma=gamma, **kw)
            clf.fit(Xtrain,ytrain.ravel()>0)  #y to vector
            res = clf.score(Xtest,ytest.ravel()>0), C, gamma
            results.append(res)  
    return max(results)

def solve():
    raw = loadmat(DATA_FOLDER+'ex6/ex6data3.mat')
    X,y=raw['X'], raw['y']
    kernel = 'rbf' #'linear', 'poly' 
    best, C, gamma = svm_best(X,y, kernel=kernel)   
    clf=svm.SVC(C=C,gamma=gamma,kernel=kernel)
    print clf
    clf.fit(X,y.ravel()>0)
    plot(X,y,clf)
    
solve()
