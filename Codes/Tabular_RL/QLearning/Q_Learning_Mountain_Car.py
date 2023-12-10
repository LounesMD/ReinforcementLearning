"""

Lounès Meddahi. lounes.meddahi@ens-rennes.fr

This file provide an implementation of the "Car-In-The-Hill" problem.
It consists of a car in the middle of two hills and try to reach the top of the one in front of it.
For this purpose, the car can either speed up or do nothing or go backwards. The car is subject to Newton's law.

State = ( X-position , Speed ) = [-1.2 , 0.6] x [-0.07 , 0.07]
init_state = ( x , 0 ) where x \in [-0.6 , -0.4]
state_t+1 = [ position_t+Speed_t+1 , Speed_t + 0.001*Action_t - cos(3*Position_t)*gravity ]

The reward is -1 for each action

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


def environnement(state, speed, action):
    """_summary_

    Args:
        position (_type_): position of the car in the Hill
        speed (_type_): speed of the car
        action (int): +1 to speed up
                      +0 do nothing
                      -1 to back up
    """
    reward = -1

    return (execution_Car(state, action), reward)


def init_state():
    x = -0.5  # x in [-0.6 , -0.4]
    return [x, 0]


def bound(state):
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
    gravity = 0.0025
    force = 0.001
    # s_t1 = state[1] + force*(action-1) - math.cos(3 * state[0])*gravity
    s_t1 = state[1] + force * (action) - gravity * (math.cos(3 * state[0]))
    new_state = [state[0] + s_t1, s_t1]

    if new_state[0] > 0.5:
        return (100, bound(new_state))

    return (-1, bound(new_state))


def final_Car(state):
    return state[0] >= 0.5  # 0.5


def ActionPossibles():
    return [-1, 0, 1]


def AllowActions(state):
    return True


from random import choices

import numpy as np


def Q_Learning(init, final, actions, execution, decision, gamma, AcceptableActions):
    """

    Parameters
    ----------
    etats : TYPE
        DESCRIPTION.
    actions : TYPE
        DESCRIPTION.
    gamma : TYPE
        DESCRIPTION.
    execution : TYPE
        DESCRIPTION.
    init : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    n_x = 19
    n_xp = 15
    min_x = -1.2
    max_x = 0.6
    min_xp = -0.07
    max_xp = 0.07
    denominateur = [(0.6 + 1.2) / n_x, (0.07 + 0.07) / n_xp]

    Q = dict()
    for i in range(n_x):
        Q[i] = dict()
        jl = list()
        for j in range(n_xp):
            Q[i][j] = dict()
            kl = list()
            for k in actions():
                Q[i][j][k] = dict()
                Q[i][j][k] = 0

    N = dict()
    for i in range(n_x):
        N[i] = dict()
        jl = list()
        for j in range(n_xp):
            N[i][j] = dict()
            kl = list()
            for k in actions():
                N[i][j][k] = dict()
                N[i][j][k] = 0

    AllActions = list()
    AllStates = list()

    laa = list()
    acc = list()
    cpt = 0
    x = list()
    y = list()

    while cpt < 4003:  # On va faire 70 épisodes
        k = 0
        s = list()
        etat_init = init()

        s.append(etat_init)
        ac = list()
        t = 0
        r = list()
        a = list()
        la = list()
        ct = 0

        while (not final(s[t])) and k < 220:
            k += 1

            actionsPossibles = list()
            for ap in actions():
                if AcceptableActions(execution(s[t], ap)[1]):
                    actionsPossibles.append(ap)

            i_disc = int((s[t][0] - min_x) / denominateur[0])
            j_disc = int((s[t][1] - min_xp) / denominateur[1])

            d = decision(
                Q, actionsPossibles, i_disc, j_disc, 1
            )  # A utiliser si on veut utiliser la manière Boltzmann
            action = choices(actionsPossibles, d, k=1)[
                0
            ]  # A utiliser si on veut utiliser la manière Boltzmann

            # action = decision(Q , actionsPossibles , s[t] , 1 ) #A utiliser si on veut utiliser la manière gloutonne

            AllActions.append(action)

            a.append(execution(s[t], action))

            r.append(a[t][0])  # le retour rt

            etat_t1 = a[t][1]

            s.append(etat_t1)  # L'état st+1

            AllStates.append(s[t])

            la.append(action)
            alpha = 1 / (1 + N[i_disc][j_disc][action])

            l = list()

            for ac in actions():
                ip = int((s[t + 1][0] - min_x) / denominateur[0])
                jp = int((s[t + 1][1] - min_xp) / denominateur[1])

                l.append(Q[ip][jp][ac])

            v = max(l)

            Q[i_disc][j_disc][action] = Q[i_disc][j_disc][action] + alpha * (
                r[t] + gamma * v - Q[i_disc][j_disc][action]
            )

            N[i_disc][j_disc][action] += 0.01

            ct += 1

            t += 1

            v2 = list()
            v1 = list()
            for elt in s:
                v1.append(elt[0])
                v2.append(elt[1])
        print(cpt, k, sum(r), max([i[0] for i in AllStates]))
        acc.append(ac)
        laa.append(la)

        y.append(len(la))
        x.append(cpt)

        cpt += 1
    return x, y, Q, AllActions, AllStates, N


gamma = 1.0
# from Algo4_QLearning import boltzmann
import matplotlib.pyplot as plt

data = list()

for i in range(1):
    v = Q_Learning(ActionPossibles, execution_Car, boltzmann, gamma, AllowActions)
    data.append(v)

for path in data:
    plt.plot(
        path[0],
        path[1],
        color="darkgrey",
        linewidth=0.4,
        markerfacecolor="black",
        markersize=5,
    )

plt.xlabel("x - Episode")

plt.ylabel("y - Number of steps to leave")

plt.title("Learning curve")


plt.show()
