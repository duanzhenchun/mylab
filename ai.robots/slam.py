from math import *
from utils import *
import random
from particle2 import particles
from robot2 import robot
import numpy as np
import matplotlib.pyplot as plt
from pid_control import twiddle


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
        #plt.plot(*zip(*data))
    return rob.reached(goal), rob.num_collisions, N, data


def run(grid, init, goal, 
         (weight_data, weight_smooth, p_gain, d_gain),
         show=True):
    from search import find_path
    import smooth_control

    grid=np.array(grid,dtype=int)
    path = find_path(grid, init, goal)
    spath = smooth_control.smooth(path, weight_data, weight_smooth)
    res = navigate(grid, init, goal, spath, 
            (p_gain, 0.0, d_gain),)
    if show:
        visual2D(path, spath, res[-1])
    return res

def average_run(params, grid, init, goal):
    K = 10
    best_err = 0.0
    for k in range(K):
        ret = run(grid, init, goal, params, show=False)
        if ret[0]:
            best_err += ret[1] * 100 + ret[2]
        else:
            best_err += 99999
    best_err /=  k+1
    return best_err


if __name__=="__main__":
#   1 = occupied space
    grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 0]]

    init = [0, 0]
    goal = [len(grid)-1, len(grid[0])-1]

    params = [weight_data, weight_smooth, p_gain, d_gain] = [0.1, 0.2, 2.0, 6.0]
    #params = twiddle(average_run, params, (grid, init, goal))
    run(grid, init, goal, params)
