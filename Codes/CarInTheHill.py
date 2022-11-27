"""

Lounès Meddahi. lounes.meddahi@ens-rennes.fr

This file provide an implementation of the "Car-In-The-Hill" problem.
It consists of a car in the middle of two hills and try to reach the top of the one in front of it.
For this purpose, the car can either speed up or do nothing or go backwards. The car is subject to Newton's law.

State = ( X-position , Speed ) = [-1.2 , 0.6] x [-0.07 , 0.07]
init_state = ( x , 0 ) where x \in [-0.6 , -0.4]
state_t+1 = [ position_t+Speed_t+1 , Speed_t + 0.001*Action_t - cos(3*Position_t) ]

The reward is -1 for each action

"""

import math

def environnement(state , speed , action):
    """_summary_

    Args:
        position (_type_): position of the car in the Hill
        speed (_type_): speed of the car
        action (int): +1 to speed up
                      +0 do nothing
                      -1 to back up 
    """

    x,xp = state[0],state[1]
    i,j = x+1.2 / 19 , xp+0.07 / 15
    
    return 0

def init_state():
    x = -0.5 # x in [-0.6 , -0.4] 
    return (x, 0)

def bound(state):
    if(state[0]<-1.2):
        state[0] = -1.2
    if(state[0]>0.6):
        state[0]=0.6
    if(state[1]>0.07):
        state[1] = 0.07
    if(state[1]<-0.07):
        state[1] = -0.07        
    return state

def execution(state , action):
    s_t1 = state[1] + 0.001*action - math.cos(3 * state[0])
    new_state = [ state[0]+s_t1   ,  s_t1   ]
    return bound(new_state)

state = init_state()
cpt = 0

while(state[0]<0.5):
    cpt += 1
    state = execution(state , 1)
    print(cpt , state)
