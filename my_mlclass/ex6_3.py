#!/usr/bin/env python

from scipy.io import loadmat
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
import re
from Stemmer import Stemmer

stem = Stemmer('en').stemWord

def plot(X, y, clf, title=None):
    data = np.append(X, y, 1)
    pos = data[data[:,2]==1]
    neg = data[data[:,2]==0]
    plt.scatter(pos[:,0], pos[:,1], marker='+', color='black')
    plt.scatter(neg[:,0], neg[:,1], marker='o', facecolor='yellow')
    
    plot_contour(data,clf)
    if title:
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


def solve(datafile, clf=None):
    raw = loadmat(datafile)
    clf = clf or svm.SVC()
    clf.fit(raw['X'], raw['y'].ravel()>0)
    plot(raw['X'], raw['y'], clf)


def find_best(raw, **kw):
    values = [.01, .03, .1, .3, 1, 3, 10, 30]
    best, best_score = None, 0
    best_score = 0
    def p(score, C, gamma):
        return 'score={} C={} gamma={}'.format(score, C, gamma)

    for C in values:
        for gamma in values:
            clf = svm.SVC(C=C, gamma=gamma, **kw)
            clf.fit(raw['X'], raw['y'].ravel()>0)
            score = clf.score(raw['Xval'], raw['yval'])
            print(p(score, C, gamma))
            if score > best_score:
                best, best_score = clf, score

    plot(raw['X'], raw['y'], clf, title=p(score, C, gamma))
    return clf


def load_voc():
    with open('ex6/vocab.txt') as fo:
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


def vectorize(text):
    voc = load_voc()
    vec = np.zeros(len(voc))
    for token in tokenize(text):
        i = voc.get(token, -1)
        if i == -1:
            continue
        vec[i] = 1
    return vec


def spam_train(clf=None):
    raw = loadmat('ex6/spamTrain.mat')
    test = loadmat('ex6/spamTest.mat')
    raw['Xval'] = test['Xtest']
    raw['yval'] = test['ytest']
    find_best(raw)


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv
    parser = ArgumentParser(description='')
    parser.add_argument('datafile')
    args = parser.parse_args(argv[1:])

    solve(args.datafile)

if __name__ == '__main__':
    main()

