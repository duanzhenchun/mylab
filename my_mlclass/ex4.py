import numpy as np
import matplotlib.pylab as plt
from util import *

def main():   
    x, y = load_sample(('ex4x.dat', 'ex4y.dat'))
    x = np.mat(np.concatenate((np.ones((x.shape[0], 1)), x), axis=1))
    theta, Js = logistic_regression(x, y, 10)

    print predict_logistic(theta, np.array([20, 80]))
    
    plt.plot(Js)
    plt.xlabel('iterations')
    plt.ylabel('cost: J')
    plt.show()
    boundary(x, y, theta)

def boundary(x, y, theta):
    y_ = y.reshape(y.size,)
    classes = (0., 1.)
    colors = ('b', 'r')
    marks = ('o', '+')
    for i, color, mark in zip(classes, colors, marks):
        plt.scatter(np.array(x)[y_ == i, 1], np.array(x)[y_ == i, 2], c=color, marker=mark)
    plt.legend(['y=%s' % i for i in classes])
    x_1 = (x[:, 1].min() - 2, x[:, 1].max() + 2)
    x_2 = -(theta[0] + theta[1] * x_1) / theta[2]
    plt.plot(x_1, x_2)
    plt.show()    
    

if __name__ == '__main__':
    main()
