import numpy as np
import matplotlib.pylab as plt
from util import *

def main():   
    X = np.loadtxt('ex/ex3x.dat')
    y = np.loadtxt('ex/ex3y.dat')
    y.shape = y.size,1
    
    X,mns,sstd = z_scale(X)
    X=addOne(X)
    alphas = [0.01, 0.03, 0.1, 0.3, 1, 1.3];    # if alpha >=1.3, no convergence result
    MAX_ITR = 100
    
    for alpha in alphas:
        theta,Js = linear_regression(X,y, MAX_ITR, alpha)
        if alpha ==1:
            theta_best = theta
        plt.plot(Js)
    plt.xlabel('iterations')
    plt.ylabel('cost: J')
    plt.legend(['alpha: %s' %i for i in alphas])
    print 'best theta in alpha:\n ', theta_best
    plt.show()

    predict(theta_best, [1650,3], mns, sstd)
    print 'normal equation:', linear_normal_equation(X,y)

def predict(theta, test, mns, sstd):
    test=(np.array(test) -mns)/sstd
    test= np.append(1,test)
    print 'predict of %s is %s' %(test, np.dot(test, theta).item())
    

if __name__ == '__main__':
    main()

