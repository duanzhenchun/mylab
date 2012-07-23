import numpy as np
from scipy.optimize import curve_fit
import pylab as pl

def func(x, a, b, c):
    return a*np.exp(-b*x) + c
    
def geny(X,a,b,c,n):    
    Y=[0,]*len(X)
    for i in range(len(X)):
        Y[i]=func(X[i],a,b,c)
        Y[i] += 0.2*np.random.normal(size=n)   
    return Y

X = np.linspace(0,4,50)
Y = geny(X, 2.5, 1.3, 0.5,5)
pl.plot(X,Y)

for i in range(len(Y[0])):
    Yi=[y[i] for y in Y]
    popt, pcov = curve_fit(func, X, Yi)
    pl.plot(popt,pcov)
pl.show()
