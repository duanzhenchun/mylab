import numpy as np
import matplotlib.pylab as plt
from util import *

    
def main():   
    x0, y = load_sample(('ex5Logx.dat', 'ex5Logy.dat'), ',')
    x = prepare(x0)
    MAX_ITR = 7
    lam = 5  # lambda
    theta, Js = logistic_regression(x,y,MAX_ITR, lam)
    print theta
    test = prepare(x0[-1].reshape(1, x0.shape[1]))
    print predict(theta, test)
    
    plt.plot(Js)
    plt.xlabel('iterations')
    plt.ylabel('cost: J')
    plt.show()
    boundary(x0, y, theta)

def boundary(x, y, theta):
    y_ = y.reshape(y.size,)
    classes = (0., 1.)
    colors = ('b', 'r')
    marks = ('o', '+')
    for i, color, mark in zip(classes, colors, marks):
        plt.scatter(np.array(x)[y_ == i, 0], np.array(x)[y_ == i, 1], c=color, marker=mark)
    
    u = np.linspace(-1, 1.5, 50)
    v = np.linspace(-1, 1.5, 50)
    z = np.zeros(shape=(len(u), len(v)))
    for i in range(len(u)):
        for j in range(len(v)):
            z[i, j] = (map_feature(np.array(u[i]), np.array(v[j])).dot(theta))
    z = z.T
    plt.contour(u, v, z)
    
    plt.legend(['y=%s' % i for i in classes] + ['Decision boundary'])
    plt.show()    
    
def prepare(x):
    return map_feature(x[:, 0], x[:, 1])
    
def predict(theta, test):
    """
    prob that class=1.0
    """
    return sigmoid(np.mat(test) * theta).item()

if __name__ == '__main__':
    main()
    
