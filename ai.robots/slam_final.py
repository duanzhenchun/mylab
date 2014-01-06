# SLAM in a rectolinear world (we avoid non-linearities)
#
# 2 dimensional world. For example, 
# if there were 2 poses and 2 landmarks, mu would look like:
#  mu =  matrix([[Px0],
#                [Py0],
#                [Px1],
#                [Py1],
#                [Lx0],
#                [Ly0],
#                [Lx1],
#                [Ly1]])
#
from math import *
import random
import numpy as np


num_landmarks      = 5        # number of landmarks
N                  = 20       # time steps
world_size         = 100.0    # size of world
measurement_range  = 50.0     # range at which we can sense landmarks
motion_noise       = 2.0      # noise in robot motion
measurement_noise  = 2.0      # noise in the measurements
distance           = 20.0     # distance by which robot (intends to) move each iteratation 


class robot:
    def __init__(self, world_size = 100.0, measurement_range = 30.0,
                 motion_noise = 1.0, measurement_noise = 1.0):
        self.measurement_noise = 0.0
        self.world_size = world_size
        self.measurement_range = measurement_range
        self.x = world_size / 2.0
        self.y = world_size / 2.0
        self.motion_noise = motion_noise
        self.measurement_noise = measurement_noise
        self.landmarks = []
        self.num_landmarks = 0

    def rand(self):
        return random.random() * 2.0 - 1.0

    def make_landmarks(self, num_landmarks):
        self.landmarks = []
        for i in range(num_landmarks):
            self.landmarks.append([round(random.random() * self.world_size),
                                   round(random.random() * self.world_size)])
        self.num_landmarks = num_landmarks

    # move: attempts to move robot by dx, dy. If outside world
    #       boundary, then the move does nothing and instead returns failure
    def move(self, dx, dy):
        x = self.x + dx + self.rand() * self.motion_noise
        y = self.y + dy + self.rand() * self.motion_noise
        if x < 0.0 or x > self.world_size or y < 0.0 or y > self.world_size:
            return False
        else:
            self.x = x
            self.y = y
            return True
    
    # sense: returns (x,y) distances to landmarks within visibility range
    #        because not all landmarks may be in this range, the list of measurements
    #        is of variable length. 
    #        Set measurement_range to -1 if you want all
    #        landmarks to be visible at all times
    def sense(self):
        Z = []
        for i in range(self.num_landmarks):
            dx = self.landmarks[i][0] - self.x + self.rand() * self.measurement_noise
            dy = self.landmarks[i][1] - self.y + self.rand() * self.measurement_noise    
            if self.measurement_range < 0.0 or abs(dx) + abs(dy) <= self.measurement_range:
                Z.append([i, dx, dy])
        return Z

    def __repr__(self):
        return 'Robot: [x=%.5f y=%.5f]'  % (self.x, self.y)


def make_trip(N, num_landmarks, world_size, measurement_range, motion_noise, 
              measurement_noise, distance):
    complete = False
    while not complete:
        data = []
        rob = robot(world_size, measurement_range, motion_noise, measurement_noise)
        rob.make_landmarks(num_landmarks)
        seen = [False for row in range(num_landmarks)]
    
        # guess an initial motion
        orientation = random.random() * 2.0 * pi
        dx = cos(orientation) * distance
        dy = sin(orientation) * distance

        for k in range(N-1):
            Z = rob.sense()
            # check off all landmarks that were observed 
            for z in Z:
                seen[z[0]] = True
            while not rob.move(dx, dy):
                # if we're out of world, pick instead a new direction
                orientation = random.random() * 2.0 * pi
                dx = cos(orientation) * distance
                dy = sin(orientation) * distance
            data.append([Z, [dx, dy]])

        # we are done when all landmarks were observed; otherwise re-run
        complete = (sum(seen) == num_landmarks)
    print 'Landmarks: ', rob.landmarks
    print rob
    return data
    
def print_result(N, num_landmarks, result):
    A=result[2*N:]
    X,Y=A[::2], A[1::2]
    print 'Estimated Landmarks:'
    for pos in zip(X,Y):
        print pos

def guess_trip(data, N, num_landmarks, motion_noise, measurement_noise):
    dim = 2* (N+num_landmarks) #2D
    Omega=np.zeros((dim,dim))
    Omega[0,0]=Omega[1,1] = 1.0

    Xi=np.zeros(dim)
    Xi[0]=Xi[1]=world_size/2.
    for k,(measurement, motion) in enumerate(data):
        # n is motion index in matrix
        n = k*2
         # update matrix by motion from i to (i+1)
        for b in range(4):
            Omega[n+b][n+b] += 1./motion_noise
        for b in range(2):
            Omega[n+b][n+b+2] -= 1.0/motion_noise
            Omega[n+b+2][n+b] -= 1.0/motion_noise
            Xi[n+b]           -= motion[b]/motion_noise
            Xi[n+b+2]         += motion[b]/motion_noise
        for z in measurement:
            # m is landmark index in matrix
            m=2*(N+z[0])
            for b in range(2):
                Omega[n+b][n+b] += 1.0/measurement_noise
                Omega[m+b][m+b] += 1.0/measurement_noise
                Omega[n+b][m+b] -= 1.0/measurement_noise
                Omega[m+b][n+b] -= 1.0/measurement_noise
                Xi[n+b]         -= z[1+b]/measurement_noise
                Xi[m+b]         += z[1+b]/measurement_noise
    #compute best estimate
    mu = np.linalg.inv(Omega).dot(Xi)
    return mu 

data = make_trip(N, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)
result = guess_trip(data, N, num_landmarks, motion_noise, measurement_noise)
print_result(N, num_landmarks, result)
