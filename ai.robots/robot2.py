import random
from math import *
import numpy as np
import scipy.stats


max_steering_angle = pi / 4.0 

steering_noise = 0.1 
distance_noise = 0.03
measurement_noise = 0.3
bearing_noise = 0.1 

class robot:
    def __init__(self, length = 0.5):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.measurement_noise = 0.0
        self.bearing_noise = 0.0 
        self.steering_drift = 0.0
        self.num_collisions = 0
        self.num_steps = 0

    def set_coordinate(self, x, y, orientation):
        self.x = float(x)
        self.y = float(y)
        self.orientation = float(orientation) % (2.0 * pi)

    def set_noise(self, s_noise=steering_noise, 
                        d_noise=distance_noise, 
                        m_noise=measurement_noise, 
                        b_noise=0.0):
        self.steering_noise = float(s_noise)
        self.distance_noise = float(d_noise)
        self.measurement_noise = float(m_noise)
        self.bearing_noise = float(b_noise)

    def set_steering_drift(self, drift):
        self.steering_drift = drift

    #checks of the robot pose collides with an obstacle, or is too far outside the plane
    def check_collision(self, grid):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    dist = sqrt((self.x - float(i)) ** 2 + 
                                (self.y - float(j)) ** 2)
                    if dist < 0.5:
                        self.num_collisions += 1
                        return False
        return True

    def check_goal(self, pos, threshold = 1.0):
        dist =  sqrt((float(pos[0]) - self.x)**2 + (float(pos[1]) - self.y)**2)
        return dist < threshold
        
    # steering = front wheel steering angle, limited by max_steering_angle
    def move(self, steering, distance, tolerance = 1e-3,):
        steering = min(max_steering_angle, steering)
        steering = max(-max_steering_angle, steering)
        distance = max(0,distance)
        # apply noise
        alpha = random.gauss(steering, self.steering_noise) # tyre steering angle
        d = random.gauss(distance, self.distance_noise) 
        # apply steering drift
        alpha += self.steering_drift
        # Execute motion
        beta = tan(alpha) * d/self.length # vehicle angle
        if abs(beta) < tolerance:
            #approximate by straight line motion
            self.x += d*cos(self.orientation)
            self.y += d*sin(self.orientation) 
            self.orientation = (self.orientation+beta)%(2.0*pi)
        else:
            # approximate bicycle model for motion
            radius = d / beta
            #(cx, cy) are circle center of vehicle movement
            cx = self.x - sin(self.orientation) * radius
            cy = self.y + cos(self.orientation) * radius
            self.orientation = (self.orientation + beta)%(2.0*pi)
            self.x = cx+(sin(self.orientation)*radius)
            self.y = cy-(cos(self.orientation)*radius) 

    def sense(self):
        return [random.gauss(self.x, self.measurement_noise),
                random.gauss(self.y, self.measurement_noise)]

    def position_prob(self, pos):
        probs = scipy.stats.norm.pdf([self.x,self.y], pos, self.measurement_noise)
        return reduce(lambda a,b:a*b, probs)

    def __repr__(self):
        return '[%.5f, %.5f, %5f]'  %(self.x, self.y, self.orientation)

    
