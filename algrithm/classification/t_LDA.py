from scipy import linalg
import numpy as np
import pylab as pl
import matplotlib as mpl
from matplotlib import colors

from sklearn.lda import LDA

class myLDA():
    """
    ref: http://blog.csdn.net/warmyellow/article/details/5454943
    two classes labels are used here. could be expended to more.
    """
    def __init__(self, class1, class2):
        all = np.concatenate((class1, class2))
        u1, u2, u = (i.mean(axis=0).T for i in (class1, class2, all))  
        Sb, Sw = np.zeros((2, 2)), np.zeros((2, 2))
        for X, c in ((class1, u1), (class2, u2)):
            Sb += (c - u) * (c - u).T * len(X)
            for x in X:
                Sw += (x.T - c) * (x.T - c).T
        Sb /= (len(class1) + len(class2))
        Sw /= len((class1, class2))
        A = np.dot(linalg.inv(Sw), Sb)
        L, V = linalg.eig(A)
        self.W = V[:, np.argmax(L)]
        self.u1, self.u2 = [np.dot(c.T, self.W)[0, 0] for c in (u1, u2)]

    def predict(self, test):
        x = np.dot(test, self.W)
        return np.argmin((abs(x - self.u1), abs(x - self.u2)))
      
def test():    
    class1 = np.mat([
        (2.9500 , 6.6300),
        (2.5300  , 7.7900),
        (3.5700 , 5.6500),
        (3.1600, 5.4700),
    ])
    class2 = np.mat([
        (2.5800 , 4.4600),
        (2.1600, 6.2200),
        (3.2700 , 3.5200),
        ])
    test = (2.81, 5.46)
    lda = myLDA(class1, class2)
    print lda.predict(test)

    lda = LDA()
    lda.fit(np.concatenate((class1, class2)), np.concatenate((np.zeros((3, 1)), np.ones((4, 1))), axis=0),
                 store_covariance=True)
    print lda.predict(test)


if __name__ == '__main__':
    test()
