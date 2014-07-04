# coding: utf-8

import math
import numpy as np
from sklearn import tree
from sklearn.ensemble import ExtraTreesRegressor
    

def dtree(X, Y):
    maxY = max(Y)
    print 'maxY:', maxY
    errs = []
    feature_w = []
    for sample, guess in sample_rotation(len(X)):
        lst = list(sample)
        clf = tree.DecisionTreeClassifier(compute_importances=True)
        clf = clf.fit([X[i] for i in lst], [Y[j] for j in lst]) 
        feature_w.append(clf.feature_importances_)
        lst2 = list(guess)
        res = clf.predict([X[i] for i in lst2])
        res2 = [Y[j] for j in lst2]
        err = 0.0
        for k in xrange(len(res)):
            bigger = max(abs(res[k]), abs(res2[k]))
            if bigger < 1e-5:
                bigger = maxY
            err += ((res[k] - res2[k]) * 1.0 / bigger) ** 2
        err /= len(res)
        errs.append(math.sqrt(err))
#     print errs
    print 'average error:',
    print '%.2f' % (sum(errs) / len(errs))
    print 'average feature weight:'
    print ['%.2f' % (i / len(feature_w)) for i in map(sum, zip(*feature_w))]

def mul_dtree(X, Y2):
    forest = ExtraTreesRegressor(n_estimators=5,
                             compute_importances=True,
                             random_state=0)
    forest.fit(X[:200], Y2[:200])
    forest.predict(X[200:])
    print Y2[200:]

def random_forest(X, Y):
    from milk.supervised import randomforest
    from milk.supervised.multi import one_against_one
    import milk.nfoldcrossvalidation
    
    features = np.array(X)   
    labels = np.array(Y) 
    rf_learner = randomforest.rf_learner()
    # rf is a binary learner, so we transform it into a multi-class classifier
    learner = one_against_one(rf_learner)
    #     learner = rf_learner
    
    # result
    # cross validate with this learner and return predictions on left-out elements
    cmat, names, preds = milk.nfoldcrossvalidation(features, labels, nfolds=4, classifier=learner, return_predictions=1)
    print 'cross-validation accuracy:', cmat.trace() / float(cmat.sum())
    return 
    
def sample_rotation(N, ratio=.25):
    def split_sample():
        for i in range(int(1 / ratio)):
            loc = map(lambda x:int(x * N * ratio), (i, i + 1))  
            yield loc
    def multirange():
        for i in xrange(0, loc[0]):
            yield i 
        for i in xrange(loc[1], N):  
            yield i  
    for loc in split_sample():
        yield multirange(), xrange(*loc)
        
def load_cocadata():
    import xlrd
    fname = '../doc/for spss 2.xlsx'
    Ylabels = u'Score    Retweet    Comment    Degree    男女比例差绝对值'.split()
    X,Y = [],[]
    data = xlrd.open_workbook(fname)
    startrow=2
    sh1 = data.sheets()[1]
    head = sh1.row_values(0)
    start,end = 'Not Campaign','Video'
    missingrow=set()
    res = []
    for i in range(head.index(start), head.index(end) + 1):
        res.append(sh1.col_values(i, start_rowx=startrow))
    for i in range(len(res[0])):
        X.append([None, ] * len(res))
    for i in range(len(res)):
        for j in range(len(res[i])):
            if not res[i][j]:
                X[j][i] = 0
            else:
                X[j][i] = int(res[i][j])
    res = []
    for i in range(head.index(Ylabels[0]), head.index(Ylabels[-1]) + 1):
        res.append(sh1.col_values(i, start_rowx=startrow))
    for i in range(len(res[0])):
        Y.append([None, ] * len(res))
    for i in range(len(res)):
        for j in range(len(res[i])):
            if res[i][j] == '':
                missingrow.add(j)
            else:
                Y[j][i] = float(res[i][j])
    for mis in sorted(missingrow,reverse=True):
        X.pop(mis)
        Y.pop(mis)
    return X, Y,Ylabels


def load_spam_trainingdata():
    """
    decision tree result:
    average error: 0.25
    average feature weight:
    ['0.04', '0.04', '0.02', '0.54', '0.14', '0.00', '0.00', '0.00', '0.07', '0.01', '0.02', '0.09', '0.04']
    sorted by order:
        days2now, followers_count, deslen, average puretxt len, ...
    
    random forest:
    very slow
    cmat:
        array([[1234,   92],
               [  65,  933]])
    accuracy: 0.93
    
    svm.SVC: fast
    accuracy: 89%
    """
    fname = '/home/whille/svnsrc/hellowhille/1/hellowhille/doc/continuedata.txt'
    Ylabels = ['is_spam',]
    X,Y = [],[]
    with open(fname) as f:
        for _ in xrange(1): # feature format 
            print f.next()
        for line in f:
            row = line.strip().split()
            x=[]
            for i in row[2:-1]:
                x.append(int(i))
            x.append(float(row[-1]))
            X.append(x)
            Y.append([int(row[1]),])
    return X, Y, Ylabels    
 
def t_svm(X,y, ratio=.25):
    """
    C, gamma of rbf, refer:
    http://scikit-learn.org/stable/modules/svm.html#parameters-of-the-rbf-kernel
    """
    from sklearn import svm
    X = np.array(X)   
    y = np.array(y)
#     l = int(len(X)*(1.0 - ratio))
#     X_trains,y_trains, Xtest, ytest = X[:l],y[:l], X[l:],y[l:]
#     best, C, gamma = svm_best(X_trains,y_trains, Xtest, ytest)
#     print 'best,C,gamma:', best,C,gamma
    C, gamma = 3, 0.3
    ave = 0.0
    for sample, guess in sample_rotation(len(X)):
        clf=svm.SVC(C=C,gamma=gamma, class_weight = 'auto')
        sample, guess = list(sample), list(guess)
        clf.fit(X[sample],y[sample])
        score=clf.score(X[guess],y[guess])
#        for i in zip(guess, clf.predict(X[guess])):
#            print i[0], i[1]
        ave += score
    print 'average score:', ave/4
#     y_= clf.predict(Xtest)
#     res = np.nonzero(ytest-y_)[0]
#     print len(res)*1.0/len(ytest)
    

def info(score, C, gamma):
    return 'score=%s C=%s gamma=%s' %(score, C, gamma)


def svm_best(X,y,Xtest,ytest, params=None, **kw):
    """
    return best params of svm:  score, C, gamma
    """
    from sklearn import svm
    params = params or (0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30,)
    results=[]
    for C in params:
        for gamma in params:  # gamma= 1 / sigma
            clf=svm.SVC(C=C,gamma=gamma, **kw)
            clf.fit(X,y.ravel()>0)  #y to vector
            res = clf.score(Xtest,ytest.ravel()>0), C, gamma
            print info(*res)
            results.append(res)
    return max(results)

    
def multi_Y(X, Y, Ylabels):
    from sklearn import preprocessing
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)     #scaler can be used later for prediction
    Y=zip(*Y)
    for i in range(len(Y)):
        print Ylabels[i], '=' * 10
        dtree(X, Y[i])
#         random_forest(X,Y[i])
#        t_svm(X,Y[i])
        
if __name__ == '__main__':
#     X, Y, Ylabels = load_cocadata()
    X,Y,Ylabels = load_spam_trainingdata()
    multi_Y(X,Y,Ylabels)
