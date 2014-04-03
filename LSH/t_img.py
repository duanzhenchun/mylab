import numpy as np
from lshash import LSHash
import matplotlib.pyplot as plt
from scipy.io import loadmat


def to_img(data):
    return np.array(data).reshape(20, 20).T

limit = 10
data = loadmat('ex3data1.mat')
X, y = data['X'], data['y']
dim=X.shape[1]
hash_size = int(np.ceil(np.log2(len(y))))
print 'hash_size:', hash_size
lsh=LSHash(hash_size, dim)
#prepare
for x in X:
    lsh.index(x)
#test
for _ in range(10):
    i = np.random.randint(0,y.shape[0])
    res = lsh.query(X[i], distance_func = 'hamming')
    n = len(res)
    fig = plt.figure()
    fig.suptitle('y=%d, found: %d' %(y[i][0]%10, n))
    n = n>limit and limit or n
    ax = fig.add_subplot(2, n, 1)
    ax.set_axis_off()
    ax.imshow(to_img(X[i]))
    ax.set_title('original img')
    for k,j in enumerate(res[:n]):
        ax = fig.add_subplot(2, n, k+1+n)
        ax.set_axis_off()
        ax.imshow(to_img(j[0]))
        ax.set_title('distance: %.2f' %j[-1])
    plt.show()

