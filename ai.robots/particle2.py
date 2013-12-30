import copy
import numpy as np
from robot2 import robot


class particles:
    def __init__( self, x, y, theta, 
              steering_noise, distance_noise, measurement_noise, 
              N = 100):
        assert N>0
        self.N = N
        self.steering_noise    = steering_noise
        self.distance_noise    = distance_noise
        self.measurement_noise = measurement_noise
        self.robs = []
        for i in range(N):
            r = robot()
            r.set_coordinate(x, y, theta)
            r.set_noise(steering_noise, distance_noise, measurement_noise)
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

    def move(self, grid, steer, speed):
        for rob in self.robs:
            rob.move(grid, steer, speed)

    def resampling(self, pos):
        w = []
        for rob in self.robs:
            w.append(rob.measurement_prob(pos))
        indices = weight_choice(w, range(self.N))
        newrobs=[]
        for i in indices:
            newrobs.append(copy.deepcopy(self.robs[i]))
        self.robs=newrobs

def weight_choice(w, lst):
    w=np.array(w)
    indices = np.random.choice(len(w),size=len(w), p=w/w.sum())
    return np.array(np.copy(lst))[indices].tolist()

# checks to see if your particle filter
# localizes the robot to within the desired tolerances
# of the true position. 
def check_output(pos, estimated_pos, tol):
    tol_xy = 15.0 
    tol_orientation = 0.25 
    error_x = abs(pos.x - estimated_pos[0])
    error_y = abs(pos.y - estimated_pos[1])
    error_orientation = abs(pos.orientation - estimated_pos[2])
    error_orientation = (error_orientation + pi) % (2.0 * pi) - pi
    correct = error_x < tol_xy and error_y < tol_xy \
              and error_orientation < tol_orientation
    return correct


def generate_ground_truth(motions):
    myrobot = robot()
    myrobot.set_noise(bearing_noise, steering_noise, distance_noise)
    Z = []
    T = len(motions)
    for t in range(T):
        myrobot.move(motions[t])
        Z.append(myrobot.sense())
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

def test():
    Iter= 10
    motions = [[2. * pi / 20, 12.],] * Iter 

    final_robot, measurements = generate_ground_truth(motions)
    estimated_position = particle_filter(motions, measurements)
    print_measurements(measurements)
    print 'Ground truth:    ', final_robot
    print 'Particle filter: ', estimated_position
    assert check_output(final_robot, estimated_position)

