#refer:
#https://www.udacity.com/course/viewer#!/c-cs373/l-48739381/e-48723601/m-48716186

import numpy as np

colors=np.array(
       [['red', 'green', 'green', 'red' , 'red'],
        ['red', 'red', 'green', 'red', 'red'],
        ['red', 'red', 'green', 'green', 'red'],
        ['red', 'red', 'red', 'red', 'red']])
obs = ['green', 'green', 'green' ,'green', 'green']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]  # by direction
sensor_right = 0.7
p_move = 0.8

def ini_belief():
    p = np.ones(colors.shape)
    return normalize(p)

def sense(prior, ob):
    hits = (colors==ob)
    # using Bayes rule
    posterior  = (hits*sensor_right + (1-hits)*(1-sensor_right))*prior 
    return normalize(posterior)

def move(p,motion):
    convolution = p_move * roll(p,*motion) + (1-p_move) * p 
    return convolution

def normalize(A):
    return A / A.sum()

def roll(A,i,j):
    A=np.roll(A,i,axis=0)
    A=np.roll(A,j,axis=1)
    return A

p=ini_belief()
for ob,motion in zip(obs,motions):
    p = move(p,motion)
    p = sense(p,ob)
print p
