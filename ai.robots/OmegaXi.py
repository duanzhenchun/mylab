import numpy as np


def doit(init_pos, move1, move2):
    Omega = np.zeros((3,3))
    Omega[0,0]=1.0
    Xi=np.zeros((3,1))
    Xi[0,0]=init_pos
    
    Omega +=np.array([[1.,-1.,0.],[-1.,1.,0.],[0,0,0]])
    Xi+=np.array([[-move1],[move1],[0.]])
    Omega +=np.array([[0.,0.,0.,],[0.,1.,-1.],[0.,-1.,1.]])
    Xi+=np.array([[0.],[-move2],[move2]])

    #best path given restrains
    mu = np.linalg.inv(Omega).dot(Xi)
    return mu

print doit(-3, 5, 3)
