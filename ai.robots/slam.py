from math import *
import random
from particle2 import particles
from robot2 import robot
import numpy as np
import matplotlib.pyplot as plt


def trace_cte(spath, index, pos):
    dx=spath[index+1][0] - spath[index][0]
    dy=spath[index+1][1] - spath[index][1]
    drx=pos[0] - spath[index][0]
    dry=pos[1] - spath[index][1]
    # u is the robot pos projectes onto the path segment
    u = (drx*dx + dry*dy)/(dx**2 + dy**2)
    # cte is the pos projected onto the normal of the path segment
    cte = (dry*dx - drx*dy)/(dx**2 + dy**2)
    return cte, u

def navigate(grid, init, goal, spath,  
             (Kp,Ki,Kd),
             print_flag = False, 
             speed = 0.1, 
             N=1000):
    start = (init[0], init[1], 0.0)
    car_length=1.0
    rob = robot(car_length)
    rob.set_coordinate(*start)
    rob.set_noise()
    filter = particles(car_length, start)

    Perr = Ierr = err= 0.0
    data=[]
    index = 0 
    while not rob.reached(goal) and N>0:
        N-=1
        Derr = -Perr
        Perr, u = trace_cte(spath, index, filter.position())
        if u>1.0: # pick the next path sgement
            index+=1
        Derr += Perr
        Ierr += Perr
        steer = -Kp* Perr -Ki* Ierr -Kd* Derr
        rob.move(steer, speed)
        filter.move(steer, speed)
        filter.resampling(rob.sense())
        data.append((rob.x, rob.y))
        if not rob.check_collision(grid):
            print '##### Collision ####'
        err += (Perr**2)
        if print_flag:
            print rob, Perr, index, u
    if print_flag:
        plt.plot(*zip(*data))
        plt.show()
    return [rob.reached(goal), rob.num_collisions, N]

def main(grid, init, goal, 
         weight_data, weight_smooth, p_gain, d_gain):
    from search import find_path
    import smooth_control

    grid=np.array(grid,dtype=int)
    path = find_path(grid, init, goal)
    spath = smooth_control.smooth(path, 0.5, 0.1)
    smooth_control.visual(path, spath)

    return navigate(grid, init, goal, spath, 
            (p_gain, 0.0, d_gain),
            print_flag=True)

#   1 = occupied space
grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]


weight_data       = 0.1
weight_smooth     = 0.2
p_gain            = 2.0
d_gain            = 6.0

    
print main(grid, init, goal, 
           weight_data, weight_smooth, p_gain, d_gain)

def twiddle(init_params):
    n_params   = len(init_params)
    dparams    = [1.0 for row in range(n_params)]
    params     = [0.0 for row in range(n_params)]
    K = 10

    for i in range(n_params):
        params[i] = init_params[i]


    best_error = 0.0;
    for k in range(K):
        ret = main(grid, init, goal, 
                   params[0], params[1], params[2], params[3])
        if ret[0]:
            best_error += ret[1] * 100 + ret[2]
        else:
            best_error += 99999
    best_error = float(best_error) / float(k+1)
    print best_error

    n = 0
    while sum(dparams) > 0.0000001:
        for i in range(len(params)):
            params[i] += dparams[i]
            err = 0
            for k in range(K):
                ret = main(grid, init, goal, 
                           params[0], params[1], params[2], params[3], best_error)
                if ret[0]:
                    err += ret[1] * 100 + ret[2]
                else:
                    err += 99999
            print float(err) / float(k+1)
            if err < best_error:
                best_error = float(err) / float(k+1)
                dparams[i] *= 1.1
            else:
                params[i] -= 2.0 * dparams[i]            
                err = 0
                for k in range(K):
                    ret = main(grid, init, goal, 
                               params[0], params[1], params[2], params[3], best_error)
                    if ret[0]:
                        err += ret[1] * 100 + ret[2]
                    else:
                        err += 99999
                print float(err) / float(k+1)
                if err < best_error:
                    best_error = float(err) / float(k+1)
                    dparams[i] *= 1.1
                else:
                    params[i] += dparams[i]
                    dparams[i] *= 0.5
        n += 1
        print 'Twiddle #', n, params, ' -> ', best_error
    print ' '
    return params


#twiddle([weight_data, weight_smooth, p_gain, d_gain])

