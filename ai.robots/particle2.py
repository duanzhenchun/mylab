import copy
import numpy as np
from robot2 import robot
from math import *
import matplotlib.pyplot as plt


class particles:
    def __init__( self, L, start, N=100):
        assert N>0
        self.N = N
        x,y,orient = start
        self.robs = []
        for i in range(N):
            r = robot(L)
            r.set_coordinate(x, y, orient)
            r.set_noise()
            self.robs.append(r)

    def position(self):
        x = 0.0
        y = 0.0
        orientation = 0.0
        for rob in self.robs:
            x += rob.x
            y += rob.y
            # orientation is tricky because it is cyclic. By normalizing
            # around the first particle we are somewhat more robust to
            # the 0=2pi problem
            orientation += (((rob.orientation
                            - self.robs[0].orientation + pi) % (2.0 * pi)) 
                            + self.robs[0].orientation - pi)
        return [x / self.N, y / self.N, orientation / self.N]

    def move(self, steer, speed):
        for rob in self.robs:
            rob.move(steer, speed)

    def resampling(self, pos):
        w = []
        for rob in self.robs:
            w.append(rob.position_prob(pos))
        indices = weight_choice(w, range(self.N))
        newrobs=[]
        for i in indices:
            newrobs.append(copy.deepcopy(self.robs[i]))
        self.robs=newrobs

    def run(self, motions, postions): 
        for motion, pos in zip(motions, postions):
            self.move(*motion)
            self.resampling(pos)
        return self.position()


def weight_choice(w, lst):
    w=np.array(w)
    indices = np.random.choice(len(w),size=len(w), p=w/w.sum())
    return np.array(np.copy(lst))[indices].tolist()

def check(pos, pos_e, tol=2.0):
    tol_orientation = 0.25 
    error_x = abs(pos.x - pos_e[0])
    error_y = abs(pos.y - pos_e[1])
    error_orientation = abs(pos.orientation - pos_e[2])
    error_orientation = (error_orientation + pi) % (2.0 * pi) - pi
    correct = error_x < tol and error_y < tol \
              and error_orientation < tol_orientation
    return correct


def generate_path(L, start, motions):
    rob = robot(L)
    rob.set_coordinate(*start)
    rob.set_noise()
    Z = []
    for motion in motions:
        rob.move(*motion)
        Z.append(rob.sense())
    return rob, Z


def test():
    car_length=5.0
    Steps = 10
    motions = [[2.*pi /20, 2.],] * Steps 
    start=[x0,y0,orient0]=[0., 0., 0.]

    final_robot, measurements = generate_path(car_length, start, motions)
    plt.plot(*zip(*measurements))
    plt.show()

    filter = particles(car_length, start)
    pos_e= filter.run(motions, measurements)

    print 'Ground truth:    ', final_robot
    print 'Particle filter: ', pos_e
    assert check(final_robot, pos_e)

if __name__=="__main__":
    test()
