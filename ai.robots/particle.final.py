from math import *
import random

max_steering_angle = pi / 4.0 
bearing_noise = 0.1 
steering_noise = 0.1 
distance_noise = 5.0 
tolerance_xy = 15.0 # Tolerance for localization in the x and y directions.
tolerance_orientation = 0.25 # Tolerance for orientation.

# the "world" has 4 landmarks.
# the robot's initial coordinates are somewhere in the square
# represented by the landmarks.
#
# NOTE: Landmark coordinates are given in (y, x) form and NOT
# in the traditional (x, y) format!

landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]] # position of 4 landmarks in (y, x) format.
world_size = 100.0 # world is NOT cyclic. Robot is allowed to travel "out of bounds"

class robot:
    def __init__(self, length = 20.0):
        self.x = random.random() * world_size # initial x position
        self.y = random.random() * world_size # initial y position
        self.orientation = random.random() * 2.0 * pi # initial orientation
        self.length = length # length of robot
        self.bearing_noise  = 0.0 # initialize bearing noise to zero
        self.steering_noise = 0.0 # initialize steering noise to zero
        self.distance_noise = 0.0 # initialize distance noise to zero

    # --------
    # set: 
    #    sets a robot coordinate
    #
    def set(self, new_x, new_y, new_orientation):
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.bearing_noise  = float(new_b_noise)
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    #    computes the probability of a measurement
    def measurement_prob(self, measurements):
        # calculate the correct measurement
        predicted_measurements = self.sense(0) # Our sense function took 0 as an argument to switch off noise.
        # compute errors
        error = 1.0
        for i in range(len(measurements)):
            error_bearing = abs(measurements[i] - predicted_measurements[i])
            error_bearing = (error_bearing + pi) % (2.0 * pi) - pi # truncate
            # update Gaussian
            error *= (exp(- (error_bearing ** 2) / (self.bearing_noise ** 2) / 2.0) /  
                      sqrt(2.0 * pi * (self.bearing_noise ** 2)))
        return error
    
    def __repr__(self): #allows us to print robot attributes.
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), 
                                                str(self.orientation))
    def move(self, motion, tolerance=1e-3):
        steering,distance = motion
        if abs(steering)>max_steering_angle:
            raise ValueError, 'Exceeded max steering angle'
        if distance<0.0:
            raise ValueError, 'Moving backwards is not valid'
        #make a new copy
        res = robot()
        res.length =self.length
        res.bearing_noise = self.bearing_noise
        res.steering_noise = self.steering_noise
        res.distance_noise = self.distance_noise
        #apply noise
        alpha = random.gauss(steering, self.steering_noise) # wheel angle
        d = random.gauss(distance, self.distance_noise) 
        #Excecute motion
        beta = tan(alpha) * d/res.length # vehicle angle
        if abs(beta)<tolerance:
            #approximate by straight line motion
            res.x = self.x + d*cos(self.orientation)
            res.y = self.y + d*sin(self.orientation) 
            res.orientation = (self.orientation+beta)%(2.0*pi)
        else:
            #approximate bicycle model for motion
            radius = d/beta
            cx = self.x - sin(self.orientation)*radius
            cy = self.y + cos(self.orientation)*radius
            res.orientation=(self.orientation+beta)%(2.0*pi)
            res.x = cx+(sin(self.orientation)*radius)
            res.y = cy-(cos(self.orientation)*radius) 
        return res

    def sense(self, add_noise=1):
        Z=[]
        for land in landmarks:
            bearings = atan2(land[0]-self.y,
                             land[1]-self.x) - self.orientation
            if add_noise:
                bearings += random.gauss(0.0, self.bearing_noise)
            Z.append(bearings % (2.0*pi))
        return Z

# extract position from a particle set
def get_position(p):
    x = 0.0
    y = 0.0
    orientation = 0.0
    for i in range(len(p)):
        x += p[i].x
        y += p[i].y
        # orientation is tricky because it is cyclic. By normalizing
        # around the first particle we are somewhat more robust to
        # the 0=2pi problem
        orientation += (((p[i].orientation - p[0].orientation + pi) % (2.0 * pi)) 
                        + p[0].orientation - pi)
    return [x / len(p), y / len(p), orientation / len(p)]

# --------
#
# The following code generates the measurements vector
# You can use it to develop your solution.
# 
def generate_ground_truth(motions):
    myrobot = robot()
    myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

    Z = []
    T = len(motions)

    for t in range(T):
        myrobot = myrobot.move(motions[t])
        Z.append(myrobot.sense())
    #print 'Robot:    ', myrobot
    return [myrobot, Z]

def print_measurements(Z):
    T = len(Z)
    print 'measurements = [[%.8s, %.8s, %.8s, %.8s],' % \
        (str(Z[0][0]), str(Z[0][1]), str(Z[0][2]), str(Z[0][3]))
    for t in range(1,T-1):
        print '                [%.8s, %.8s, %.8s, %.8s],' % \
            (str(Z[t][0]), str(Z[t][1]), str(Z[t][2]), str(Z[t][3]))
    print '                [%.8s, %.8s, %.8s, %.8s]]' % \
        (str(Z[T-1][0]), str(Z[T-1][1]), str(Z[T-1][2]), str(Z[T-1][3]))

# --------
#
# The following code checks to see if your particle filter
# localizes the robot to within the desired tolerances
# of the true position. The tolerances are defined at the top.
#

def check_output(final_robot, estimated_position):
    error_x = abs(final_robot.x - estimated_position[0])
    error_y = abs(final_robot.y - estimated_position[1])
    error_orientation = abs(final_robot.orientation - estimated_position[2])
    error_orientation = (error_orientation + pi) % (2.0 * pi) - pi
    correct = error_x < tolerance_xy and error_y < tolerance_xy \
              and error_orientation < tolerance_orientation
    return correct


def particle_filter(motions, measurements, N=500): # I know it's tempting, but don't change N!
    # Make particles
    p = []
    for i in range(N):
        r = robot()
        r.set_noise(bearing_noise, steering_noise, distance_noise)
        p.append(r)
    # Update particles
    for t in range(len(motions)):
        # motion update (prediction)
        p2 = []
        for i in range(N):
            p2.append(p[i].move(motions[t]))
        p = p2
        # measurement update
        w = []
        for i in range(N):
            w.append(p[i].measurement_prob(measurements[t]))
        # resampling
        p3 = []
        index = int(random.random() * N)
        beta = 0.0
        mw = max(w)
        for i in range(N):
            beta += random.random() * 2.0 * mw
            while beta > w[index]:
                beta -= w[index]
                index = (index + 1) % N
            p3.append(p[index])
        p = p3
    return get_position(p)

 
Iter= 10
motions = [[2. * pi / 20, 12.],] * Iter 

final_robot, measurements = generate_ground_truth(motions)
estimated_position = particle_filter(motions, measurements)
print_measurements(measurements)
print 'Ground truth:    ', final_robot
print 'Particle filter: ', estimated_position
assert check_output(final_robot, estimated_position)
