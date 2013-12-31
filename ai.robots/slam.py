from math import *
import random
from particle2 import particles
from robot2 import robot
from plan import plan


def navigate(grid, goal, spath, params, printflag = False, speed = 0.1, timeout = 1000):
    start=(x0,y0,orient0)=(0., 0., 0.)
    car_length=1.0
    rob = robot()
    rob.set_coordinat(*start)
    rob.set_noise()
    filter = particles(car_length, start)

    cte  = 0.0
    err  = 0.0
    N    = 0
    index = 0 # index into the path
    while not rob.check_goal(goal) and N < timeout:
        diff_cte = - cte
        # compute the CTE
        estimate = filter.get_position()
        dx=spath[index+1][0] - spath[index][0]
        dy=spath[index+1][1] - spath[index][1]
        drx=estimate[0] - spath[index][0]
        dry=estimate[1] - spath[indeex][1]
        # u is the robot estimate projectes onto the path segment
        u = (drx*dx + dry*dy)/(dx**2 + dy**2)
        # cte is the estimate projected onto the normal of the path segment
        cte =(dry*dx - drx*dy)/(dx**2 + dy**2)
        # pick the next path sgement
        if u>1.0:
            index+=1
        
        diff_cte += cte
        steer = - params[0] * cte - params[1] * diff_cte 
        rob.move(steer, speed)
        filter.move( steer, speed)

        pos = rob.sense()
        filter.resampling(pos)

        if not rob.check_collision(grid):
            print '##### Collision ####'

        err += (cte ** 2)
        N += 1

        if printflag:
            print rob, cte, index, u

    return [rob.check_goal(goal), rob.num_collisions, rob.num_steps]

def main(grid, init, goal, 
     weight_data, weight_smooth, p_gain, d_gain):

    path = plan(grid, init, goal)
    path.astar()
    path.smooth(weight_data, weight_smooth)
    return navigate(grid, goal, path.spath, [p_gain, d_gain])

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

