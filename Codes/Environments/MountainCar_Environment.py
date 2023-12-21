"""
This file provide an implementation of the "Car-In-The-Hill" problem.
It consists of a car in the middle of two hills and try to reach the top of the one in front of it.
For this purpose, the car can either speed up or do nothing or go backwards. The car is subject to Newton's law.

State = ( X-position , Speed ) = [-1.2 , 0.6] x [-0.07 , 0.07]
init_state = ( x , 0 ) where x \in [-0.6 , -0.4]
state_t+1 = [ position_t+Speed_t+1 , Speed_t + 0.001*Action_t - cos(3*Position_t)*gravity ]

The reward is -1 for each action.
"""

import math


def boltzmann(Q, actions, i, j, to):
    """
    Fonction qui va choisir une action à faire en utilisant le modèle de Boltzmann

    Parameters
    ----------
    Q : list
        Fonction qualitée.
    actions : list
        Actions possibles.
    s : list
        coordonnées.
    to : int
        température .

    Returns
    -------
    l : list
        (Renvoie une distribution de probabilité des actions en suivant le modele de Boltzmann).

    """
    l = list()
    for action in actions:
        p = 0
        ex = math.exp((Q[i][j][action]) / to)
        v = 0
        for a in actions:
            v += math.exp((Q[i][j][a]) / to)
        p = ex / v
        l.append(p)
    return l


def init_state():
    """Return the initial state of the car

    Returns:
        list : initial state
    """
    x = -0.5  # x in [-0.6 , -0.4]
    return [x, 0]


def bound(state):
    """
    Return the state bounded by the limits of the environnement

    Args:
        state (list): actual state

    Returns:
        list : bounded state
    """
    if state[0] < -1.2:
        state[0] = -1.2
    if state[0] > 0.6:
        state[0] = 0.6
    if state[1] > 0.07:
        state[1] = 0.0699999999999
    if state[1] < -0.07:
        state[1] = -0.0699999999999
    return state


def execution_Car(state, action):
    """Return the new state of the car after executing the action

    Args:
        state (list): actual state
        action (int): +1 to speed up
                      +0 do nothing
                      -1 to back up

    Returns:
        list : new state
    """
    gravity = 0.0025
    force = 0.001
    s_t1 = state[1] + force * (action) - gravity * (math.cos(3 * state[0]))
    new_state = [state[0] + s_t1, s_t1]

    if new_state[0] > 0.5:
        return (100, bound(new_state))

    return (-1, bound(new_state))


def final_Car(state):
    """Return True if the car is in the top of the hill

    Args:
        state (list): actual state

    Returns:
        Bool : True if the car is in the top of the hill
    """
    return state[0] >= 0.5


def ActionPossibles():
    """
        Return the list of possible actions

    1 : Accelerate
    0 : Do nothing
    -1 : Back up
    """
    return [-1, 0, 1]


def AllowActions(action, state):
    """return True for all actions because all actions are allowed in this problem

    Args:
        state (_type_): actual state
        action (_type_): action to do


    Returns:
        Bool: True
    """
    return True
