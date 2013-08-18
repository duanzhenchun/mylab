import numpy as np
import matplotlib.pylab as plt
from util import *

    
def main():   
    x0, y = load_sample(('ex5Logx.dat', 'ex5Logy.dat'), ',')
    x = prepare(x0)
    MAX_ITR = 7
    Lambda = 5 
    theta, Js = logistic_regression(x,y,MAX_ITR, Lambda)
    print theta
    test=x0[-1]
    test.shape=1, test.size
    test = prepare(test)
    print predict_logistic(theta, test, False)
    
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
    
if __name__ == '__main__':
    main()
    
