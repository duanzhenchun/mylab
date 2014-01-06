from math import *
import random
import matplotlib.pyplot as plt

def pid_run((Kp,Ki,Kd), 
             start, 
             speed=1.0, 
             N=200,
             print_flag = False):
    """
    Proportional: to achieve target
    Integral: to eliminate system err
    Derivative: to avoid oscillation
    """
    from robot import robot
    rob = robot()
    rob.set_coordinate(*start)
    rob.set_noise(0.1,0.1)
    rob.set_steering_drift(10./180*pi) #10 degree system erro
    radius = start[1]
    Perr = racetrack_cte(rob.x, rob.y, radius)
    Ierr=0.0
    err=0.0
    data=[]
    for i in range(N*2):
        Derr = -Perr
        Perr = racetrack_cte(rob.x, rob.y, radius)
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

# racetrack cross check error
def racetrack_cte(x, y, radius):
    if x < radius:
        cte = sqrt((x -radius)**2 +(y -radius)**2) - radius
    elif x > 3.0* radius:
        cte = sqrt((x -3.0 * radius)**2 +(y -radius)**2) -radius
    elif y>radius:
        cte = y - 2.0 * radius
    else:
        cte = -y
    return cte

def twiddle(fn, init_params, (args), tol=1e-5):
    n_params = len(init_params)
    params = init_params
    dparams = [1.,] * n_params
    best_err = fn(params, *args)
    print 'best error:', best_err

    n = 0
    while sum(dparams) > tol:
        for i in range(n_params):
            params[i] += dparams[i]
            err = fn(params, *args)
            if err < best_err:
                best_err = err
                dparams[i] *= 1.1
            else:
                params[i] -= 2.0 * dparams[i]
                err = fn(params, *args)
                if err < best_err:
                    best_err = err 
                    dparams[i] *= 1.1
                else:
                    params[i] += dparams[i]
                    dparams[i] *= 0.9
        n += 1
        print 'Twiddle #%d' %n, params, ' --> ', best_err
    return params

def t_twiddle():
    start = (0.0, 1.0,0.0)
    init_params=[0,]*3
    best=twiddle(pid_run, init_params, (start,))
    print best
    pid_run(best, (0.0,1.0,0.0), True)
    
def racetrack():
    radius = 25.0
    params = [5.0, 0.01, 20.0]
    err = pid_run(params,(0,radius, pi/2.0),N=1000, print_flag=True)
    print 'Final paramaeters: ', params, '\n ->', err

if __name__ == '__main__':
    t_twiddle()
    racetrack()
