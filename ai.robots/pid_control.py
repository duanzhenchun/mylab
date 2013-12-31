from math import *
import random
import matplotlib.pyplot as plt
from robot2 import robot

def pid_run((Kp,Ki,Kd), start, speed=1.0, print_flag = False):
    """
    Proportional: to achieve target
    Integral: to eliminate system err
    Derivative: to avoid oscillation
    """
    rob = robot()
    rob.set_coordinate(*start)
    rob.set_noise(0.1,0.1)
    rob.set_steering_drift(10./180*pi) #10 degree system erro
    N = 200
    radius = start[1]
    Perr = rob.cte(radius)
    Ierr=0.0
    err=0.0
    data=[]
    for i in range(N*2):
        Derr = -Perr
        Perr = rob.cte(radius)
        Derr += Perr
        Ierr += Perr
        steer = -Kp* Perr -Ki* Ierr -Kd* Derr
        rob.move(steer, speed)
        data.append((rob.x, rob.y))
        if i>=N:
            err += Perr **2
    if print_flag:
        plt.plot(*zip(*data))
        plt.show()
    return err/N 
    
def twiddle(start, tol=1e-5):
    n_params=3
    params = [0,] * n_params
    dparams = [1.,] * n_params
    best_err= pid_run(params,start)
    n=0
    while sum(dparams)>tol:
        for i in range(n_params):
            params[i]+=dparams[i]
            err=pid_run(params,start)
            if err<best_err:
                best_err=err
                dparams[i]*=1.1
            else:
                params[i] -=2.0*dparams[i]
                err=pid_run(params,start)
                if err<best_err:
                    best_err=err
                    dparams[i]*=1.1
                else:
                    params[i]+=dparams[i]
                    dparams[i]*=0.9
        n+=1
        #print 'Twiddle #', n, params, ' --> ', best_err
    return params

def t_twiddle():
    start = (0.0, 1.0,0.0)
    best=twiddle(start)
    print best
    pid_run(best, (0.0,1.0,0.0), True)
    
def racetrack():
    radius = 25.0
    params = [5.0, 0.001, 20.0]
    err = pid_run(params,(0,radius, pi/2.0),True)
    print '\nFinal paramaeters: ', params, '\n ->', err

if __name__ == '__main__':
    #t_twiddle()
    racetrack()
