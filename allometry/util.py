import pylab as plt
import math
import numpy as np

def calclinalg(x, y, show=False):
    x, y = np.array(x), np.array(y)
    x = x.reshape((len(x), x.size / len(x)))
    x0 = np.ones((len(x), 1))
    # y = b0.x0 + b1.x1 + b2.x2 + ...
    #refer: http://mail.scipy.org/pipermail/numpy-discussion/2011-March/055461.html
    x = np.concatenate((x0, x), axis=1)
    res = np.linalg.lstsq(x, y)
    c, m = res[0][0], res[0][1:]
    print m, c
    x = x[:, 1:]
    if show:
        plt.plot(x, y, 'o', label='Original data', markersize=10)
        plt.plot(x, m * x + c, 'r', label='Fitted line')
        plt.legend()
        plt.show()
    return m

