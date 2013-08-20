from ex6_3 import *
from util import *


def svm_best(X,y):
    values = (0.01,0.1,1,10,100, 1000)

    cut=int(X.shape[0] * 0.6)
    Xtrain, Xtest = np.split(X,(cut,))
    ytrain, ytest = np.split(y,(cut,))
            
    results=[]
    for C in values:
        for gamma in values:  # gamma= 1/sigma
            clf=svm.SVC(C=C,gamma=gamma)
            clf.fit(Xtrain,ytrain.ravel()>0)  #y to vector
            res = clf.score(Xtest,ytest.ravel()>0), C, gamma
            print res
            results.append(res)  
    return max(results)

def solve():
    raw = loadmat(DATA_FOLDER+'ex6/ex6data2.mat')
    X,y=raw['X'], raw['y']
    best, C, gamma = svm_best(X,y)    
    clf=svm.SVC(C=C,gamma=gamma)
    clf.fit(X,y.ravel()>0)
    plot(X,y,clf)
    
solve()
