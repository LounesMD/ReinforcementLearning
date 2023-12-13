import random

import numpy as np


def epsilon_greedy(Q, state):
    # return random.choices( [np.argmax(Q[state[0]][state[1]]) , random.choice([0 , 1])] , weights=(0.9 , 0.1) , k=1)[0]
    return np.argmax(Q[state[0]][state[1]][state[2]][state[3]])


def epsilon_greedy(state, cpt, epsilon, Q):
    if cpt < 500:
        return random.choice([0, 1])
    val = np.random.random()

    if cpt > 7000:
        epsilon = 0.999 * epsilon

    if val < epsilon:
        return random.choice([0, 1])
    else:
        return np.argmax(Q[state[0]][state[1]][state[2]][state[3]])
