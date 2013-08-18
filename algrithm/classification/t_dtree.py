#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from sklearn import tree
from sklearn.ensemble import ExtraTreesRegressor
    
def cocodata():
    import xlrd
    data = xlrd.open_workbook('../doc/Cocacola top 200 20130803.xlsx')
    sh1 = data.sheets()[0]
    head = sh1.row_values(0)
    start = 'Photo'
    end = 'Co-branding'
    res = []
    for i in range(head.index(start), head.index(end) + 1):
        res.append(sh1.col_values(i, start_rowx=1))
    X = []
    for i in range(len(res[0])):
        X.append([None, ] * len(res))
    for i in range(len(res)):
        for j in range(len(res[i])):
            if not res[i][j]:
                X[j][i] = 0
            else:
                X[j][i] = int(res[i][j])
        Y_score = sh1.col_values(head.index('Score'), start_rowx=1)
    for i in range(len(Y_score)):
        try:
            Y_score[i] = float(Y_score[i])
        except:
            Y_score[i] = 0.0
            
    Y_gender = sh1.col_values(head.index('Male'), start_rowx=1)
    for i in range(len(Y_gender)):
        if not Y_gender[i]:
            Y_gender[i] = 0.5

    Y_sen = sh1.col_values(head.index('Sentiment'), start_rowx=1)
    for i in range(len(Y_sen)):
        if not Y_sen[i]:
            Y_sen[i] = 0
        elif Y_sen[i] != 0:
            Y_sen[i] = 1
    Y_level = sh1.col_values(head.index(u'层级'), start_rowx=1)
    for i in range(len(Y_level)):
        if not Y_level[i]:
            Y_level[i] = 0
    Y_retweets = sh1.col_values(head.index(u'转发数'), start_rowx=1)
    return X, (Y_score, Y_gender, Y_sen, Y_level, Y_retweets)

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
    print 'ave error:',
    print '%.2f' % (sum(errs) / len(errs))
    print 'ave feature weight:'
    print ['%.2f' % (i / len(feature_w)) for i in map(sum, zip(*feature_w))]

def mul_dtree(X, Y2):
    forest = ExtraTreesRegressor(n_estimators=5,
                             compute_importances=True,
                             random_state=0)
    forest.fit(X[:200], Y2[:200])
    forest.predict(X[200:])
    print Y2[200:]

def sample_rotation(N, ratio=.2):
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
        
if __name__ == '__main__':
    X, Ys = cocodata()
    Ylables = 'Score', 'Male', 'Sentiment', 'retweet level', 'retweet num'
    for i in range(len(Ys)):
        print Ylables[i], '=' * 10
        dtree(X, Ys[i])
