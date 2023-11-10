# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 09:28:28 2021

@author: Lounès Meddahi

Quality Function based algorithm :

The purpose of the SARSA algorithm (on-policy) is to compute the Quality function. 
The on-policy algorithms use the action done instead of the best action.

So instead of :  max_{a \in Actions} Q(s* , a) 
      we have :  Q(s* , a*)
Where s* is the state the agent is and a* the action on this state
"""


from random import choice
from random import choices

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
import math

from Utile import *


def Sarsa(etats, actions, gamma, environnement, init, decision, execution, final):
    """
    Parameters
    ----------
    etats : TYPE
        DESCRIPTION.
    actions : TYPE
        DESCRIPTION.
    gamma : TYPE
        DESCRIPTION.
    environnement : TYPE
        DESCRIPTION.
    init : TYPE
        DESCRIPTION.
    decision : TYPE
        DESCRIPTION.
    execution : TYPE
        DESCRIPTION.
    final : TYPE
        DESCRIPTION.

    Returns
    -------
    x : TYPE
        DESCRIPTION.
    y : TYPE
        DESCRIPTION.
    Q : TYPE
        DESCRIPTION.

    """
    # Q va nous permettre de stocker la qualité pour tous les couples (etat , action) sous forme de matrice
    eps = 50

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

    laa = list()
    # N va nous permettre de calculer le taux d'apprentissage pour  chaque
    N = list()
    for i in range(ligne):
        jl = list()
        for j in range(colonne):
            kl = list()
            for k in range(len(actions())):
                kl.append(0)
            jl.append(kl)
        N.append(jl)

    cpt = 0
    x = list()
    y = list()

    while cpt < 70:
        la = list()
        observation = list()  # Liste des choses à observer
        s = list()  # Liste des états successifs
        a = list()  # listes des actions émises
        r = list()
        s.append(init())
        t = 0
        actionsPossibles = list()

        for ap in actions():
            if execution(s[t], ap)[0] != -100:
                actionsPossibles.append(ap)

        """
        #Action Si on utilise Eps       
        a.append( decision(Q , actionsPossibles , s[t] , eps ) ) 
        e = execution(s[t] , a[t] )
        observation.append( e  )  
        """

        # Action si on veut utiliser Boltzmann
        d = decision(Q, actionsPossibles, s[t], 0.5)  # Cas Boltzmann
        a.append(choices(actionsPossibles, d, k=1)[0])
        observation.append(execution(s[t], a[t]))

        while not final(
            s[t]
        ):  # Temps que l'épisode n'est pas fini (donc que s[t] n'est pas l'état final)
            r.append(observation[t][0])  # le retour rt
            s.append(observation[t][1])  # L'état st+1
            la.append(a[t])

            # On va maintenant choisir l'action à émettre at+1
            actionsPossibles = list()
            for ap in actions():
                if execution(s[t + 1], ap)[0] != -100:
                    actionsPossibles.append(ap)

            # Cas Boltzmann
            d = decision(Q, actionsPossibles, s[t + 1], 0.5)
            a.append(choices(actionsPossibles, d, k=1)[0])
            observation.append(execution(s[t + 1], a[t + 1]))

            """
            #Cas Eps
            a.append( decision(Q , actionsPossibles , s[t+1] , eps ) ) 
            e = execution(s[t+1] , a[t+1] )
            observation.append( e  )  
            """

            # print( observation[t+1] , s[t+1] , a[t+1])

            alpha = 1 / (1 + N[s[t][1]][s[t][0]][a[t]])

            Q[s[t][1]][s[t][0]][a[t]] = Q[s[t][1]][s[t][0]][a[t]] + alpha * (
                r[t]
                + gamma * Q[s[t + 1][1]][s[t + 1][0]][a[t + 1]]
                - Q[s[t][1]][s[t][0]][a[t]]
            )

            N[s[t][1]][s[t][0]][a[t]] += 0.1
            t += 1

            # print(t , cpt)
            # print(s[t])
            # affichage2_0(maze , s[t] , [10,11])
        eps = eps / 2
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
    v = Sarsa(
        etats_labyrinthe,
        actions_labyrinthe,
        0.9,
        maze,
        init_labyrinthe,
        boltzmann,
        exectution_labyrinthe,
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


# Affichage de la HeatMap
"""
QModifier = Sarsa(etats_labyrinthe , actions_labyrinthe , 0.9 , maze , init_labyrinthe , Eps_Gloutonne , exectution_labyrinthe , est_final_labyrinthe)[2]

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
