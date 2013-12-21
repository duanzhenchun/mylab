from math import *
import random
import matplotlib.pyplot as plt

class robot:
    def __init__(self, length = 20.0):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    def set_coordinate(self, x, y, orientation):
        self.x = float(x)
        self.y = float(y)
        self.orientation = float(orientation) % (2.0 * pi)

    def set_noise(self, s_noise, d_noise):
        # this is often useful in particle filters
        self.steering_noise = float(s_noise)
        self.distance_noise = float(d_noise)

    def set_steering_drift(self, drift):
        self.steering_drift = drift

    # move: 
    #    steering = front wheel steering angle, limited by max_steering_angle
    def move(self, steering, distance, 
             tolerance = 1e-3, max_steering_angle = pi / 4.0):
        steering = min(max_steering_angle, steering)
        steering = max(-max_steering_angle, steering)
        distance = max(0,distance)
        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)
        # apply steering drift
        steering2 += self.steering_drift
        # Execute motion
        turn = tan(steering2) * distance2 / self.length
        if abs(turn) < tolerance:
            # approximate by straight line motion
            self.x += distance2 * cos(self.orientation)
            self.y += distance2 * sin(self.orientation)
            self.orientation = (self.orientation + turn) % (2.0 * pi)
        else:
            # approximate bicycle model for motion
            radius = distance2 / turn
            cx = self.x - (sin(self.orientation) * radius)
            cy = self.y + (cos(self.orientation) * radius)
            self.orientation = (self.orientation + turn) % (2.0 * pi)
            self.x = cx + (sin(self.orientation) * radius)
            self.y = cy - (cos(self.orientation) * radius)

    def cte(self, radius):
        if self.x < radius:
            cte = sqrt((self.x -radius) **2 +(self.y -radius) **2) - radius
        elif self.x > 3.0* radius:
            cte = sqrt((self.x -3.0 * radius) **2 +(self.y -radius) **2) -radius
        elif self.y>radius:
            cte = self.y - 2.0 * radius
        else:
            cte = -self.y
        return cte


    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]'  % (self.x, self.y, self.orientation)

def pid_run((Kp,Ki,Kd), start, print_flag = False):
    """
    Proportional: to achieve target
    Integral: to eliminate system err
    Derivative: to avoid oscillation
    """
    rob = robot()
    rob.set_coordinate(*start)
    rob.set_noise(0.1,0.1)
    rob.set_steering_drift(10./180*pi) #10 degree system erro
    speed = 1.0 
    time_interval = 1.0
    N = 100
    err=0.0
    Ierr=0.0
    Perr = rob.y
    data=[]
    for i in range(N*2):
        Derr = rob.y - Perr
        Perr = rob.y
        Ierr += Perr
        steer = -Kp* Perr -Ki* Ierr -Kd* Derr
        rob.move(steer, speed*time_interval)
        data.append((rob.x, rob.y))
        if i>=N:
            err += Perr **2
    if print_flag:
        plt.plot(*zip(*data))
        plt.show()
    return err/N 
    
def twiddle(start,tol=1e-2):
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
    
def t_cte():
    radius = 25.0
    params = [10.0, 15.0, 0]
    err = pid_run(params,(0,radius, pi/2.0),True)
    print '\nFinal paramaeters: ', params, '\n ->', err

if __name__ == '__main__':
    t_twiddle()
    t_cte()
