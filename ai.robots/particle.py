from math import *
import random

max_steering_angle = pi / 4.0 
bearing_noise = 0.1 
steering_noise = 0.1 
distance_noise = 0.03
measurement_noise = 0.3

# the "world" has 4 landmarks.
# the robot's initial coordinates are somewhere in the square
# represented by the landmarks.
landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]] 
world_size = 100.0 # world is NOT cyclic. Robot is allowed to travel "out of bounds"





def particle_filter(motions, measurements, N=500): 
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
            # p2.check_collision(grid)
        p = p2
        # measurement update
        w = []
        for i in range(N):
            w.append(p[i].measurement_prob(measurements[t]))
        # resampling
        p = weight_choice(w,p)
    return get_position(p)

