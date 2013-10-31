#ref: http://www.puffinwarellc.com/index.php/news-and-articles/articles/33-latent-semantic-analysis-tutorial.html?start=2

from numpy import zeros, asarray, sum, dot
from scipy.linalg import svd, diagsvd
from math import log


titles = [
    "The Neatest Little Guide to Stock Market Investing",
    "Investing For Dummies, 4th Edition",
    "The Little Book of Common Sense Investing: The Only Way to Guarantee Your Fair Share of Stock Market Returns",
    "The Little Book of Value Investing",
    "Value Investing: From Graham to Buffett and Beyond",
    "Rich Dad's Guide to Investing: What the Rich Invest in, That the Poor and the Middle Class Do Not!",
    "Investing in Real Estate, 5th Edition",
    "Stock Investing For Dummies",
    "Rich Dad's Advisors: The ABC's of Real Estate Investing: The Secrets of Finding Hidden Profits Most Investors Miss"
]
stopwords = ['and', 'edition', 'for', 'in', 'little', 'of', 'the', 'to']
ignorechars = ''',:'!'''

class LSA(object):
    def __init__(self, stopwords, ignorechars):
        self.stopwords = stopwords
        self.ignorechars = ignorechars
        self.wdict = {}
        self.dcount = 0

    def parse(self, doc):
        words = doc.split();
        for w in words:
            w = w.lower().translate(None, self.ignorechars)
            if w in self.stopwords:
                continue
            elif w in self.wdict:
                self.wdict[w].append(self.dcount)
            else:
                self.wdict[w] = [self.dcount]
        self.dcount += 1

    def build(self):
        self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        self.keys.sort()
        self.A = zeros([len(self.keys), self.dcount])
        for i, k in enumerate(self.keys):
            for d in self.wdict[k]:
                self.A[i, d] += 1

    def printA(self):
        print self.A

    def TFIDF(self):
        WordsPerDoc = sum(self.A, axis=0)
        DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
        rows, cols = self.A.shape
        for i in range(rows):
            for j in range(cols):
                self.A[i, j] = (self.A[i, j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])

    def calc(self):
        self.U, self.S, self.Vt = svd(self.A, full_matrices=False)
#        for index in xrange(3, len(self.S)):
#            self.S[index] = 0
#        A1 = dot(dot(self.U, diagsvd(self.S, len(self.S), len(self.Vt))), self.Vt)
#        self.U, self.S, self.Vt = svd(A1, full_matrices=False)

mylsa = LSA(stopwords, ignorechars)
for t in titles:
    mylsa.parse(t)
mylsa.build()
mylsa.printA()
mylsa.TFIDF()
mylsa.calc()

import pylab
shapes = 'so'
Ts = ['T%d' % (i + 1) for i in range(len(titles))]
A = ((mylsa.U, mylsa.keys), (mylsa.Vt.T, Ts))
#for i in range(len(A)):
#    for j in range(A[i][0].shape[0]):
#        (x, y) = A[i][0][j, 1:3]
#        pylab.plot(x, y, shapes[i])
#        pylab.text(x, y, A[i][1][j])
for i in range(len(mylsa.A)):
    x, y = mylsa.A[i][0], mylsa.U[i][0]
    pylab.plot(x, y, 'o')
    pylab.text(x, y, mylsa.keys[i])
print i
pylab.show()
