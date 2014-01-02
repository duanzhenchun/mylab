import numpy as np
import matplotlib.pyplot as plt


def visual2D(*args):
    for A in args:
        A=np.array(A)
        plt.plot(A[:,0],A[:,1], 'o-')
    plt.show()
