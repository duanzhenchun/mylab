# coding: utf-8
import numpy as np
from sklearn import svm
from sklearn import preprocessing


class SVMer(object):
    def __init__(self):
        self.cls()
        self.scaler = None
        C, gamma = 3, 0.3  # grid test values
        self.clf = svm.SVC(C=C, gamma=gamma, class_weight='auto')
    
    def fit(self):
        X, y = self.pre()
        self.clf.fit(X, y)
        self.cls()
    
    def predict(self):
        X, y = self.pre()
        print 'svm training score:', self.clf.score(X, y)
        self.scaler = None
        
    def judge(self, threshold=0.8):
        X, y = self.pre()
        self.cls()
        if X != None:
#            return self.clf.predict(X)[0]
            res = self.clf.predict_proba(X)[:,1]
            return (res>threshold)*1
        else:
            return -1
    
    def stats(self):
        from sklearn.metrics import f1_score
        X, y = self.pre()
        y_ = self.clf.predict(X)
        self.cls()
        return [f1_score(y, y_, average=ave) for ave in ('micro', 'macro')]

    def add(self, X, y, uid):
        self.X.append(X)
        self.y.append(y)
        self.uids.append(uid)
        
    def pre(self):
        try:   
            X = np.array(self.X, dtype=float)   
        except Exception, e:
            print self.X 
            print self.uids
            self.cls()
            raise e
        y = np.array(self.y)
        if not self.scaler:
            self.scaler = preprocessing.StandardScaler().fit(X)
        try:
            X = self.scaler.transform(X)  # scaler can be used later for prediction
        except:
            print 'transform error, X is:' , X
            self.cls()
            return None, None
        return X, y
    
    def cls(self):
        self.X, self.y, self.uids = [], [], []
