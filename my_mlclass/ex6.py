#!/usr/bin/env python


#ref: https://bitbucket.org/tebeka/ml-class/src/a03c2ba7f4d6?at=default

from scipy.io import loadmat
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
import re
from Stemmer import Stemmer
from util import *

stem = Stemmer('en').stemWord


def plot(X, y, clf, title=''):
    data = np.append(X, y, 1)
    pos = data[data[:,2]==1]
    neg = data[data[:,2]==0]
    plt.scatter(pos[:,0], pos[:,1], marker='+', color='black')
    plt.scatter(neg[:,0], neg[:,1], marker='o', facecolor='yellow')
    
    plot_contour(data,clf)
    plt.title(title)
    plt.show()    
    
    
def plot_contour(data, clf): 
    u = np.linspace(data[:,0].min(), data[:,0].max(), 100)
    v = np.linspace(data[:,1].min(), data[:,1].max(), 100)
    z = np.zeros(shape=(len(u), len(v)))
    for i in range(len(u)):
        for j in range(len(v)):
            z[i, j] = clf.predict([u[i], v[j]])[0]
    plt.contour(u, v, z.T)


def info(score, C, gamma):
    return 'score=%s C=%s gamma=%s' %(score, C, gamma)
        
def svm_best(X,y,Xtest,ytest, params=None, **kw):
    """
    return best params of svm:  score, C, gamma
    """
    params = params or (0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30)
    results=[]
    for C in params:
        for gamma in params:  # gamma= 1 / sigma
            clf=svm.SVC(C=C,gamma=gamma, **kw)
            clf.fit(X,y.ravel()>0)  #y to vector
            res = clf.score(Xtest,ytest.ravel()>0), C, gamma
            print info(*res)
            results.append(res)  
    return max(results)
    
    
def solve(fdata, ftest=None, kernel='rbf'):
    """
    kernels: 'rbf', 'linear', 'poly', ... doc in svm.SVC 
    """
    raw = loadmat(DATA_FOLDER+ fdata)
    X,y = raw['X'], raw['y']
    if ftest:
        raw = loadmat(DATA_FOLDER+ ftest)
        Xtest,ytest = raw['Xtest'], raw['ytest']
    else:
        X,y,Xtest,ytest = self_test(X,y)
    best, C, gamma = svm_best(X,y,Xtest,ytest, kernel=kernel)   
    clf=svm.SVC(C=C,gamma=gamma,kernel=kernel)
    clf.fit(X,y.ravel()>0)
    print clf
    plot(X,y,clf, title=info(best, C, gamma))
    return clf
    
    
def load_voc(fname):
    with open(fname) as fo:
        kv = (line.split() for line in fo)
        return dict((v.strip(), int(k)) for k, v in kv)


def normailze(text):
    text = text.lower()
    text = re.sub('<[^<>]+>', ' ', text)
    text = re.sub('[0-9]+', 'number', text)
    text = re.sub('(http|https)://[^\s]*', 'httpaddr', text)
    text = re.sub('[^\s]+@[^\s]+', 'emailaddr', text)
    text = re.sub('\$+', 'dollar', text)
    return text


def tokenize(text):
    text = normailze(text)
    tokens = re.split(r'[ @$/#.\-:&*+=\[\]?!(){},\'">_<;%\n\r]', text)
    tokens = (re.sub('[^a-zA-Z]', '', token) for token in tokens)
    return (stem(token) for token in tokens if token.strip())


def vectorize(voc, text):
    vec = np.zeros(len(voc))
    for token in tokenize(text):
        i = voc.get(token, -1)
        if i == -1:
            continue
        vec[i] = 1
    return vec


def spam_train():
    return solve('ex6/spamTrain.mat',ftest= 'ex6/spamTest.mat')
    
    
def test_email(C=1, gamma=0.01):
    raw = loadmat(DATA_FOLDER+ 'ex6/spamTrain.mat')
    X,y = raw['X'], raw['y'].ravel()>0
    clf=svm.SVC(C=C,gamma=gamma)
    clf.fit(X,y)
    print clf.score(X,y)
    
    voc = load_voc(DATA_FOLDER+'ex6/vocab.txt')
    for ftest in ('emailSample1.txt', 'emailSample2.txt', 'spamSample1.txt','spamSample2.txt'):
        with open(DATA_FOLDER+'ex6/'+ ftest) as f:
            text = f.read()
            x = vectorize(voc, text)  
            print ftest, clf.predict(x)

        
if __name__ == '__main__':
#    solve('ex6/ex6data2.mat')
#    solve('ex6/ex6data3.mat', 'poly')
#    spam_train()
    test_email()

