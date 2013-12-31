steering_noise = 0.1 
distance_noise = 0.03
measurement_noise = 0.3
bearing_noise = 0.1 

# the "world" has 4 landmarks.
# the robot's initial coordinates are somewhere in the square
# represented by the landmarks.
landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]] 
world_size = 100.0 # world is NOT cyclic. Robot is allowed to travel "out of bounds"
