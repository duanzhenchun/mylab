import numpy as np
from matplotlib import pyplot as plt

def costL(x,y):
    return (1.0-x)**2 + 100.0*(y-x**2)**2

def gradient(x,y):
    dx = -2.0* x + 400.0 *(x**2-y) * x
    dy = 200.0 * (y-x**2)
    return dx, dy


def GD(steps=10**2, learn_rate=1e-3, tol=1e-3):
    x,y = np.random.normal(size=(2))
    #x=y=2.0
    res=[]
    for step in xrange(steps):
        dx, dy = gradient(x,y)
        x -= learn_rate * dx
        y -= learn_rate * dy
        e = costL(x,y)
        #print step, e
        res.append(e)
        old_e = e
        if e < tol:
            break
    print e
    plt.plot(res)
    plt.show()
    return x,y

def f(x, *args):
    u, v = x
    return costL(u,v)

def gradf(x, *args):
    u, v = x
    gu,gv=gradient(u,v)
    return np.asarray((gu, gv))

def t_min():
    from scipy import optimize
    x0=np.random.rand(2)   # Initial guess.
    return optimize.fmin_cg(f, x0, fprime=gradf)

print t_min()
print GD()
