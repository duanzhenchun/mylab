#encoding:utf-8
from dbmgr import dbmanager
from tools import *


def getsents(f):
    blk_lst = []
    remain = u''
    for line in f:
        line = line.replace(' ', '').replace('　', '')
        sens, tail = split_sens(line)
        if sens:
            sens[0] = remain + sens[0]
            blk_lst += sens
        remain = tail
    if remain:
        blk_lst.append(remain)
    return blk_lst


def iter_en_sens(ppath, target='.txt'):
    for fname in iter_fname(ppath, target):
        logging.info(fname)
        sens = []
        for sen in iter_single_en(open(fname, 'r')):
            yield sen


def iter_single_en(f):
    for line in f:
        line = line.replace('　', '') #chinese space
        sens = split_sens_en(line)
        if sens:
            yield sens

def count_cs(ppath):
    count = 0
    for line in iter_lines(ppath):
        for w in line:
            if is_cs(w):
                count += 1
    return count

not_end = u'[a-zA-Z0-9，\u4e00-\u9fa5]'
u_space = u'[ 　]+'


import pickle
def savepkl(dic, dname):
    f = file(dname + '.pkl', 'wb')
    pickle.dump(dic, f)
    f.close()

def loadpkl(dname):
    f = file(dname + '.pkl', 'rb')
    dic = pickle.load(f)
    f.close()
    return dic

def iter_dics(out, high):
    for i in xrange(1, high):
        dname = out + os.sep + 'dic_%dw' % (i + 1)
        yield loadpkl(dname), dname


def saveall(dic, out):
    db = dbmanager(to_unicode(out))
    db.saveall(dic)
    del db

def load_dic(out):
    db = dbmanager(to_unicode(out))
    return db.getall()
    del db

def clean_dic(out):
    db = dbmanager(to_unicode(out))
    return db.clean()

def plot_w(dic, name):
    import pylab

    X = pylab.frange(0, len(dic) - 1)
    Y = list(sorted(dic.values(), reverse=True))
    Y = map(lambda y:pylab.log(y), Y)
    pylab.plot(X, Y)
    #show()
    pylab.savefig(name + '.png')

def plot_dic_cmp(dic, imgname, firstnum):
    import pylab

    X = pylab.frange(0, len(dic) - 1)
    Ys = list(sorted(dic.values(), key=lambda lis:sum(lis), reverse=True))
    for i in xrange(len(Ys[0])):
        Y = [y[i] for y in Ys]
        pylab.plot(X[:firstnum], Y[:firstnum])
    pylab.savefig(imgname + '_%d.png' % firstnum)

def merged(dics):
    dic_sum = {}
    for d in dics:
        dic_sum.update(d)
    return dic_sum

def cmp_dics(dics):
    dic_cmp = merged(dics)
    for k in dic_cmp:
        for d in dics:
            if k not in d:
                d[k] = 0
    for k in dic_cmp:
        dic_cmp[k] = [d[k] for d in dics]
    return dic_cmp



import hashlib
def filemd5(fname):
    txt = open(fname, 'rb').read()
    m = hashlib.md5()
    m.update(txt)
    return m.hexdigest()

def get_dulps():
    return g_dulps

import os
def _is_dulp(fname, rec, md5rec, dulps):
    """rec possible dulplicate file in files, and output them in folder
       dulplic condition: same fname or md5sum
       return: is dulplic or not
    """
    rela = rela_name(fname)
    if rela in rec:
        dulps[rela] = fname
    elif os.path.exists(fname):     #tolerate none exist file
        digest = filemd5(fname)
        if digest in md5rec:
            print 'dulp file', fname
            dulps[rela] = fname
            return True
        else:
            md5rec[digest] = fname
    else:
        rec[rela] = fname
    return False

def is_dulp(fnames):
    rec, md5rec, dulps = {}, {}, {}
    for fname in fnames:
        _is_dulp(fname, rec, md5rec, dulps)
    return dulps

g_rec, g_md5rec, g_dulps = {}, {}, {}


def dulp_dec(iter_f):
    global g_rec, g_md5rec, g_dulps
    def _(*a, **kw):         # func args
        for fname in iter_f(*a, **kw):
            if not _is_dulp(fname, g_rec, g_md5rec, g_dulps):
                yield fname
    return _


def allsub(ws):
    for i in range(len(ws)):
        head, remain = ws[:i + 1], ws[i + 1:]
        if len(remain) <= 0:
            yield head
        for p in allsub(remain):
            yield head + '|' + p


class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance


def singularmaker():
    import inflect
    p = inflect.engine()
    def wrapper(word):
        return p.singular_noun(word)
    return wrapper
singular_teller = singularmaker()


def ispluralw(k):
    to = singular_teller(k)
    if to and to != k:
        return to
    return None


def isupperw(k):
    if k.isupper():
        to = k[0] + k[1:].lower()
        return to
    return None


def plotxy(x, y):
    import matplotlib.pyplot as plt
    import numpy as np
    x = np.array(x)
    y = np.array(y)
    A = np.vstack([x, np.ones(len(x))]).T
    (m, c), residuals = np.linalg.lstsq(A, y)[:2]
    plt.plot(x, y, 'o')
    plt.plot(x, m * x + c, 'r', label='Fitted line')
    plt.legend()
    plt.show()
    return residuals[0]


def plot_diff(X, Y):
    import matplotlib.pyplot as plt
    plt.plot(range(len(X)), map(lambda x:x - X[0], X), 'g-',
             range(len(Y)), map(lambda y:y - Y[0], Y), 'b+'
            )
    plt.show()


debug = False
t_en = [u'Baratheon', u'Theon']
t_cs = [u'拜拉席恩', u'席恩']

"""
x=[1855, 3703, 3753, 27889, 29522, 46153, 75929, 77632, 133482, 150157, 162140]
y=[7, 710, 1356, 1385, 10563, 11138, 16986, 28180, 28754, 50055, 56744, 61520]

y=kx+c  k~=0.38
for i in range(1,len(x)):
    if abs((y[i]-y[i-1] ) -2.6*(x[i]-x[i-1])) < 10:
                        
for i in range(1,len(y)-1):
    print plotxy(x,y[:i]+y[i+1:])
    
    
巴 [401, 54, 599356]
利 [1757, 185, 597768]
斯 [3044, 963, 598806]
坦 [411, 21412, 595323]
巴利斯坦 [35, 88810, 547425] 458615 3.17336455192e+11  4 1.69662466791e+11

"""
