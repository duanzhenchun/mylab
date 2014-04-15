import numpy as np
import matplotlib.pyplot as plt

s=np.linspace(0,1)
def s_curve(s, r,b):
    return 1. - (1. - s**r)**b

def t_s_curve():
    parames = [(3,10), (6,20), (5, 50)]
    for r,b in parames:
        plt.plot(s,np.vectorize(lambda x:s_curve(x,r,b))(s))
    plt.legend(parames)
    plt.show()

def Pand(p,r):
    return p**r

def Por(p,b):
    return 1-(1-p)**b

def t_Ffamily():
    for p in (.8, .2):
        print Por(Pand(p,4),4), Pand(Por(p,4),4)

