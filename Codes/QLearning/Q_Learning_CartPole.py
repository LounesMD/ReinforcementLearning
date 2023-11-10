"""

Lounès Meddahi.

"""

import math
import sys

import sys
import os
from matplotlib.pyplot import savefig
from Codes.Environments.Cart_Pole import *
from Codes.ActionSelection.boltzmann import *
import random
from random import choices
import numpy as np


def render_cart(cart, k, d, action):
    state = cart.get_state()
    x = state[0]
    theta = state[2]
    velocity = state[1]
    angular_velocity = state[3]

    cart_length = cart.length

    line1.set_offsets([cart.position, 0])

    line2.set_xdata([x, x + cart_length * math.sin(theta)])
    line2.set_ydata([0, cart_length * math.cos(theta)])
    line3.set_text(
        "Angle "
        + str(round(cart.pole_angle, 4))
        + " Position "
        + str(round(cart.position, 4))
        + " Episode "
        + str(k)
        + " Epoch "
        + str(d)
        + " Action "
        + str(action)
    )

    fig.canvas.draw()
    fig.canvas.flush_events()


def Q_Learning(decision, gamma, cart):
    # Genreate me the doc of this function

    actions = cart.get_possible_actions()
    eps = 0.2
    nb = 20
    # Q-table and N-table of size 20x20x20x20 so I'm sure there will be enough cells
    Q = dict()
    for i in range(nb):  # position_disc):
        Q[i] = dict()
        for j in range(nb):  # velocity_disc):
            Q[i][j] = dict()
            for l in range(nb):  # pole_angle_disc):
                Q[i][j][l] = dict()
                for k in range(nb):  # pole_angular_velocity_disc):
                    Q[i][j][l][k] = dict()
                    for a in actions:
                        Q[i][j][l][k][a] = dict()
                        Q[i][j][l][k][a] = 0

    N = dict()
    for i in range(nb):  # position_disc):
        N[i] = dict()
        for j in range(nb):  # velocity_disc):
            N[i][j] = dict()
            for l in range(nb):  # pole_angle_disc):
                N[i][j][l] = dict()
                for k in range(nb):  # pole_angular_velocity_disc):
                    N[i][j][l][k] = dict()
                    for a in actions:
                        N[i][j][l][k][a] = dict()
                        N[i][j][l][k][a] = 0

    AllActions = list()
    AllStates = list()

    laa = list()
    acc = list()
    cpt = 0
    x = list()
    y = list()

    while cpt < 20000:  # On va faire 70 épisodes
        k = 0
        s = list()
        etat_init = cart.get_state()

        s.append(etat_init)
        ac = list()
        t = 0
        r = list()
        a = list()
        la = list()
        ct = 0
        retour = 0

        while cart.Terminated == False:
            k += 1
            actionsPossibles = list()
            for ap in actions:
                actionsPossibles.append(ap)  # All actions are possible

            (
                pos_disc,
                vel_disc,
                p_ang_disc,
                p_ang_vel_disc,
            ) = CartPoleDiscretizer().discretize([s[t][0], s[t][1], s[t][2], s[t][3]])

            d = decision(
                Q,
                actionsPossibles,
                [pos_disc, vel_disc, p_ang_disc, p_ang_vel_disc],
                0.95,
            )  # A utiliser si on veut utiliser la manière Boltzmann

            action = choices(actionsPossibles, d, k=1)[
                0
            ]  # A utiliser si on veut utiliser la manière Boltzmann

            # action = action_selection([p_ang_disc , p_ang_vel_disc , p_ang_disc , p_ang_vel_disc] , Q , cpt , 20000)

            # action = np.argmax(Q[pos_disc][vel_disc][p_ang_disc][p_ang_vel_disc])
            # if np.random.random() < exploration_rate(cpt) :
            #     action = random.choice([0 , 1])

            # action = decision(Q , actionsPossibles , s[t] , 1 ) #A utiliser si on veut utiliser la manière gloutonne
            # action = epsilon_greedy([pos_disc , vel_disc , p_ang_disc , p_ang_vel_disc], cpt)
            AllActions.append(action)
            reward = cart.action(action)
            new_state = cart.get_state()

            a.append([reward, new_state])

            r.append(a[t][0])  # le retour rt
            retour += r[t]
            etat_t1 = a[t][1]

            s.append(etat_t1)  # L'état st+1

            AllStates.append(s[t])

            la.append(action)
            alpha = 1 / (
                1 + N[p_ang_disc][p_ang_vel_disc][p_ang_disc][p_ang_vel_disc][action]
            )

            l = list()

            for ac in actions:
                ip, jp, ipp, jpp = CartPoleDiscretizer().discretize(
                    [s[t + 1][0], s[t + 1][1], s[t + 1][2], s[t + 1][3]]
                )
                l.append(Q[ip][jp][ipp][jpp][ac])
            v = max(l)
            alpha = 0.1

            Q[pos_disc][vel_disc][p_ang_disc][p_ang_vel_disc][action] += alpha * (
                r[t]
                + gamma * v
                - Q[pos_disc][vel_disc][p_ang_disc][p_ang_vel_disc][action]
            )

            N[pos_disc][vel_disc][p_ang_disc][p_ang_vel_disc][action] += 0.01

            ct += 1

            t += 1

            v2 = list()
            v1 = list()
            for elt in s:
                v1.append(elt[0])
                v2.append(elt[1])
            # render_cart(cart , cpt , k)
            if cpt % 500 == 0:
                render_cart(cart, cpt, k, action)
        if cpt % 500 == 0:
            print(cpt, k, retour, action)

        cart.reset()
        acc.append(ac)
        laa.append(la)

        y.append(len(la))
        x.append(cpt)

        cpt += 1
    return x, y, Q, AllActions, AllStates, N


##########################################################################################


gamma = 0.97
# from Algo4_QLearning import boltzmann
import matplotlib.pyplot as plt

data = list()


for i in range(1):
    cart = CartPole()

    plt.ion()
    x = cart.position
    cart_length = cart.length
    theta = cart.pole_angle

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim((-4.8, 4.8))
    ax.set_ylim((-0.5, 1.2))
    line1 = ax.scatter([cart.position], [0], marker="s", color="black", label="Cart")
    line3 = ax.set_title(
        "Cart-Pole Environment : Angle "
        + str(round(cart.pole_angle, 4))
        + " Position "
        + str(round(cart.position, 4))
    )

    ax.plot([-2.4, 2.4], [0, 0], color="blue", linewidth=2, label="Track")
    ax.scatter([-2.4, 2.4], [0, 0], color="blue")
    (line2,) = ax.plot(
        [x, x + cart_length * math.sin(theta)],
        [0, cart_length * math.cos(theta)],
        color="brown",
        label="Pole",
    )
    fig.show()

    v = Q_Learning(boltzmann, gamma, cart)
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
