import numpy as np
import matplotlib.pylab as plt
from util import *

def main():   
    x0,y = load_sample(('ex5Linx.dat', 'ex5Liny.dat'))
    plt.scatter(x0,y)
    x = polynomial_linear(x0)
#    x,mns,sstd = z_scale(x)

    theta_normal = linear_normal_equation(x,y, 1.0)
    print 'normal equation:'
    print theta_normal
    plot_fitting(theta_normal)
    plt.show()  
    m,n=x.shape 
    alphas = ( 0.01, 0.03, 0.1, 0.3, 1, 1.3 )    # if alpha >=1.3, no convergence result
    lambdas = (0, 1, 10)
    MAX_ITR = 100 
    for lam in lambdas:
        for alpha in alphas:
            theta,Js = linear_regression(x,y, MAX_ITR, alpha, lam)    
            if alpha==0.03 and lam==1:
                theta_best = theta
            plt.plot(Js)
        plt.xlabel('iterations')
        plt.ylabel('cost: J')
        plt.legend(['alpha: %s' %i for i in alphas])
        plt.show()

    print 'best theta in alpha:\n ', theta_best
    test = x0[-1]
    test.shape=test.size,1
    test = polynomial_linear(test)
    print 'predict of %s is %s' %(test, predict_linear(theta, test))

def plot_fitting(theta):
    x0 = np.arange(-1,1,0.05)
    x0.shape = x0.size,1
    x = polynomial_linear(x0)
    y= x.dot(theta)
    plt.plot(x0,y,'--')


if __name__ == '__main__':
    main()

