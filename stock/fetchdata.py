#coding=utf8
import re
import datetime
import numpy as np
import pylab as pl
from matplotlib import finance
from matplotlib.collections import LineCollection
from sklearn import cluster, covariance, manifold
import cPickle as pickle
import time

#china stocks list: http://quote.eastmoney.com/stocklist.html
NAME_CODE = '(.*?)\((.*)\)'
Markets = {'ss': 1, 'sz': -1}
SEP = ' '
WAIT_TIME = 30
d1 = datetime.datetime(2010, 01, 01)
d2 = datetime.datetime(2014, 01, 01)


def gen_symbols(lines, mar, idx):
    market = lines[idx].strip().decode('utf8')
    for info in market.split(' '):
        res = re.search(NAME_CODE, info)
        if not res:
            print 'quote not match', info
        name, code = res.groups()
        assert name and code
        symbol = '%s.%s' % (code, mar)
        yield symbol, name


def get_quotes():
    import urllib2
    from socket import error as SocketError
    import errno

    fi = open('china.txt')
    lines = fi.readlines()
    symbol_dict = {}
    for mar, idx in Markets.iteritems():
        for k, v in gen_symbols(lines, mar, idx):
            symbol_dict[k] = v
    quotes = []
    symbols = []
    #symbol e.g.: u'603099.ss',u'002281.sz'

    for symbol in symbol_dict.keys():
        try:
            q = finance.quotes_historical_yahoo(symbol, d1, d2, asobject=True)
            #q.readlines(), return format: Date,Open,High,Low,Close,Volume,Adj Close
        except Exception, e:
            print symbol, e
            symbol_dict.pop(symbol)
        if None != q:
            quotes.append(q)
            symbols.append(symbol)
    """
        except urllib2.HTTPError, e:
            if e.code == 404:
                print symbol, 'not exist'
            else:
                raise e
        except urllib2.URLError, e:
            if 'Connection reset by peer' in e.reason:
                wait(symbol)
                i-=1
                continue
        except SocketError as e:
            if e.errno == errno.ECONNRESET:
                wait()
                i-=1
                continue
            else:
                raise e
        except Exception, e:
            raise e
    """
    return symbol_dict, symbols, quotes


def wait(symbol):
    print symbol, 'sleep %d sec and try again' % WAIT_TIME
    time.sleep(WAIT_TIME)


def alldate(quotes):
    allds = set()
    for q in quotes:
        allds.update(q.date)
    return sorted(allds)


def add_missing(quotes):
    newds = alldate(quotes)
    N, M = len(quotes), len(newds)
    variation = np.zeros((N, M), dtype=np.float)
    for n, q in enumerate(quotes):
        J = len(q)
        m, j = 0, 0
        while m < M and j < J:
            while q.date[j] != newds[m] and m < M:
                print n, m, j, newds[m], q.date[j]
                m += 1
            else:
                variation[n, m] = q.close[j] - q.open[j]
            m += 1
            j += 1
    return variation


def save():
    symbol_dict, symbols, quotes = get_quotes()
    pickle.dump(symbol_dict, open('symbol_dict.pkl', 'w'))
    pickle.dump(symbols, open('symbols.pkl', 'w'))
    pickle.dump(quotes, open('quotes.pkl', 'w'))


def load():
    symbol_dict = pickle.load(open('symbol_dict.pkl'))
    symbols = pickle.load(open('symbols.pkl'))
    quotes = pickle.load(open('quotes.pkl'))
    return symbol_dict, symbols, quotes


def main():
    symbol_dict, symbols, quotes = load()
    variation = add_missing(quotes)
    X = variation.copy().T
    for n in xrange(len(quotes)):
        t = X[:, n].std()
        if t > 0:
            X[:, n] /= t
    abnormal = np.where(X.sum(axis=0) == 0)
    X = np.delete(X, abnormal, 1)
    edge_model = covariance.GraphLassoCV(tol=1e-2, max_iter=40)
    edge_model.fit(X)


save()
