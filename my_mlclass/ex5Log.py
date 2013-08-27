import matplotlib.pylab as plt
from util import *

    
def main():   
    X0 = np.loadtxt('ex/ex5Logx.dat', delimiter=',')
    y = np.loadtxt('ex/ex5Logy.dat', delimiter=',')
    X = prepare(X0)
    Lambda = 5 
    res = logistical_min(X, y, Lambda)
    theta=res.x
    test=X0[-1]
    test.shape=1, test.size
    test = prepare(test)
    print predict_logistic(theta, test, False)
    
    boundary(X0, y, theta)

def boundary(X, y, theta):
    y_ = y.reshape(y.size,)
    classes = (0., 1.)
    colors = ('b', 'r')
    marks = ('o', '+')
    for i, color, mark in zip(classes, colors, marks):
        plt.scatter(np.array(X)[y_ == i, 0], np.array(X)[y_ == i, 1], c=color, marker=mark)

    def fn((ui,vj)):
        return map_feature(np.array(ui), np.array(vj)).dot(theta)
    plt.contour(*calc_contour(X, fn))
    
    plt.legend(['y=%s' % i for i in classes] + ['Decision boundary'])
    plt.show()    
    
def prepare(X):
    return map_feature(X[:, 0], X[:, 1])
    
if __name__ == '__main__':
    main()
    
