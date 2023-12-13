# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 11:56:12 2021

@author: Lounès Meddahi

Quality Function based algorithm :

The Q(λ) algorithm uses the eligibility of a tupple (action , state) made at time t on time t+k.
"""
from random import choice, choices

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
import math

from Utile import *


def Q_Lambda(
    etats, actions, gamma, lambd, environnement, init, execution, decision, alpha, final
):
    """
    Fonction Q(λ)

    Parameters
    ----------
    etats : list
        liste des états possibles.
    actions : list
        Liste des actions possibles.
    gamma : int
        valeur dépréciée.
    lambd : int
        valeur lamda.
    environnement : list
        environnement (labyrinthe) dans le quel l'agent va évoluer.
    init : function
        fonction qui donne l'état initial.
    execution : function
        fonction qui permet d'executer une action dans l'environnement
    decision : function
        foncion qui permet de donner une probabilité aux actions possibles (boltzmann , eps-gloutonne, etc).
    alpha : int
        DESCRIPTION.
    final : function
        fonction qui permet de savoir si l'état passé en paramètre est un état final ou non.

    Returns
    -------
    x : TYPE
        DESCRIPTION.
    y : TYPE
        DESCRIPTION.
    Q : TYPE
        DESCRIPTION.

    """

    ligne = len(environnement)
    colonne = len(environnement[0])

    Q = list()
    for i in range(ligne):
        jl = list()
        for j in range(colonne):
            kl = list()
            for k in range(len(actions())):
                kl.append(0)
            jl.append(kl)
        Q.append(jl)
    cpt = 0
    x = list()
    y = list()
    laa = list()

    while cpt < 70:
        la = list()
        # Cette fonction e(s,a) va nous permettre de connaitre l'éligibilité d'une paure etat-action
        E = list()
        for i in range(ligne):
            jl = list()
            for j in range(colonne):
                kl = list()
                for k in range(len(actions())):
                    kl.append(0)
                jl.append(kl)
            E.append(jl)

        t = 0
        r = list()  # Liste des retours possibles
        d = list()
        s = list()
        a = list()  # Dans a on stock les actions successives
        observation = list()  # Dans observation on stock les couples retour-etatt+1
        # Etat initial
        s.append(init())

        actionsP = list()
        for ap in actions():
            if execution(s[t], ap)[0] != -100:
                actionsP.append(ap)

        d = decision(Q, actionsP, s[t], 0.5)
        a.append(choices(actionsP, d, k=1)[0])
        observation.append(execution(s[t], a[t]))
        while not final(s[t]):
            # Là on va émettre l'action at et observer rt-st+1
            r.append(observation[t][0])  # le retour rt
            s.append(observation[t][1])  # L'état st+1
            # affichage2_0(maze , s[t] , [10,11])
            la.append(a[t])
            # On va choisir l'action at+1 à émettre dans st+1
            actionsPossibles = list()
            # print(s[t] , s[t+1])
            for ap in actions():
                if execution(s[t + 1], ap)[0] != -100:
                    actionsPossibles.append(ap)

            # Cas Boltzmann
            d = decision(Q, actionsPossibles, s[t + 1], 0.5)
            a.append(choices(actionsPossibles, d, k=1)[0])
            observation.append(execution(s[t + 1], a[t + 1]))

            #################################################################################
            # On va chercher le a*
            l = list()
            # print(actionsPossibles)
            for action in actionsPossibles:
                l.append((Q[s[t + 1][1]][s[t + 1][0]][action], action))
            a_opti = max(l, key=lambda x: x[0])[1]
            #################################################################################
            delta = (
                r[t]
                + gamma * Q[s[t + 1][1]][s[t + 1][0]][a_opti]
                - Q[s[t][1]][s[t][0]][a[t]]
            )

            E[s[t][1]][s[t][0]][a[t]] += 1

            for etat in etats():
                for action in actions():
                    Q[etat[1]][etat[0]][action] = (
                        Q[etat[1]][etat[0]][action]
                        + alpha * delta * E[etat[1]][etat[0]][action]
                    )
                    E[etat[1]][etat[0]][action] = (
                        gamma * lambd * E[etat[1]][etat[0]][action]
                    )
            t += 1

        cpt += 1
        laa.append(la)
        x.append(cpt)
        y.append(len(la))
    print(
        len(laa[-1])
    )  # Cela va nous permettre de connaitre le nombre de pas fait pour le dernier épisode
    return x, y, Q


################################################---AFFICHAGE---#############################################################

# Affichage de la Learning Curve
data = list()
for i in range(15):
    v = Q_Lambda(
        etats_labyrinthe,
        actions_labyrinthe,
        0.9,
        0.9,
        maze,
        init_labyrinthe,
        exectution_labyrinthe,
        boltzmann,
        0.85,
        est_final_labyrinthe,
    )
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

# 0.6 -> 0.9 -> 0.3

# Affichage de la HeatMap
"""
QModifier = Q_Lambda(etats_labyrinthe , actions_labyrinthe , 0.9 , 0.9 , maze , init_labyrinthe ,exectution_labyrinthe,  boltzmann , 0.85 , est_final_labyrinthe)[2]

il = list()
for i in range(16):
    jl = list()
    for j in range(16):
        jl.append(max(QModifier[j][i]))
    il.append(jl)
uniform_data = il
ax = sns.heatmap(uniform_data)
"""

###########################################################################################################################
