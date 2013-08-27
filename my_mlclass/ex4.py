import numpy as np
import matplotlib.pylab as plt
from util import *


def main():   
    x0, y0 = load_sample(('ex4x.dat', 'ex4y.dat'))
    train_errs, cv_errs = [], []    
    ts = np.dot(x0.shape[0] / 8, range(1, 8)).tolist()
    for t in ts:
        print t
        X, X_cv = np.split(x0, (t,))
        y, y_cv = np.split(y0, (t,))
        X = addOne(X)
        X_cv = addOne(X_cv)
        res = logis_fmin(X,y)
        print res.x
        theta, Js = logistic_regression(X, y, 4)
        train_errs.append(Js[-1])
        cv_errs.append(logist_cost(X_cv, y_cv, theta))
        # print predict_logistic(theta, np.array([20, 80]))
    
    print ts
    print train_errs
    plt.plot(ts, train_errs)
    plt.plot(ts, cv_errs)
    plt.xlabel('iterations')
    plt.ylabel('cost: J')
    plt.legend(('train_errs', 'cv_errs'))
    plt.show()
    boundary(X, y, theta)

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
