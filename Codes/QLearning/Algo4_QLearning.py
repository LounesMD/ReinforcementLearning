# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 11:03:04 2021

@author: Lounès

Quality Function based algorithm :

The purpose of the Q-Learning algorithm is to compute the optimal policy of an agent on an environnement where the reward and transition functions are unknown.
The steps are :

°) Random initialisation of the Quality Function (for each (state, action))
    1) From the current state 's', choose the action 'a' to do
    2) Perform the action 'a' and observe the reward 'r' and the new state 's*'
    3) Update Q
    4) Repeat

In order to choose the action to do in the step 1), I've implemented 3 functions :
1) Random choice
2) Greedy choice
3) Blotzmann 
"""
import time
from random import choice
from random import choices
import math
import matplotlib.pyplot as plt
import numpy as np


"""
Pour l'algorithme de Q-learning qui va suivre, on va partir du fait que chaque action nous permet d'avoir un retour.
Par exemple, pour l'exemple du labyrinthe, on va gagner 0 point à chaque fois qu'on va arriver sur une cellule qui va 
nous rapprocher de la fin, et  -100 points si on va sur un mur (ce sera un critère pour vérifier si une action est possibles ou non).

Pour savoir si notre épisode est finie, on va partir du principe qu'il faut utiliser une fonction qui détermine si l'état dans le quel on se trouve est final ou non.
"""


#####################################Fonctions utiles#####################################
def conversion(c):
    """
    Fonction qui permet de convertir le caractère c en un certain nombre
    """
    if c == "*":
        return -100
    elif c == " ":
        return 0
    elif c == "O":
        return -1
    elif c == "V":
        return 100


file = open("../Environments/Maze.txt", "r")

maze = list()
for line in file:
    l = list()
    for character in line:
        if character != "\n":
            l.append(conversion(character))
    maze.append(l)

maze.reverse()  # Ce la va nous permettre d'avoir le (0,0) en bas à gauche de notre labyrinthe


def etats_labyrinthe():
    """
    On va définir tous les états possibles du labyrinthe. Ce qui correspond aux coordonnées du plateau
    """
    l = list()
    for i in range(16):
        for j in range(16):
            l.append([i, j])
    return l


def actions_labyrinthe():
    """
    Cette fonction va nous permettre d'avoir la liste des actions possibles pour le jeu du labyrinthe.
    On va supposer que:
        0 -> aller à droite
        1 -> aller en haut
        2 -> aller à droite
        3 -> aller en bas
    Returns
    -------
    list
        actions.
    """
    return [0, 1, 2, 3]


def exectution_labyrinthe(etat, action):
    """
    fonction qui va permettre d'executer l'action passer en paramètre dans l'environnement du labyrinthe et renvoyer:
        (retour , etat) qui sont les choses à observer une fois l'action effectuée
    """
    p = etat.copy()
    if action == 0:
        if p[1] + 1 > len(maze[0]) - 1:
            return (maze[p[0]][p[1]], p)
        p[1] += 1
        return (maze[p[0]][p[1]], p)
    if action == 1:
        if p[0] + 1 > len(maze) - 1:
            return (maze[p[0]][p[1]], p)
        p[0] += 1
        return (maze[p[0]][p[1]], p)
    if action == 2:
        if p[1] - 1 < 0:
            return (maze[p[0]][p[1]], p)
        p[1] -= 1
        return (maze[p[0]][p[1]], p)
    if action == 3:
        if p[0] - 1 < 0:
            return (maze[p[0]][p[1]], p)
        p[0] -= 1
        return (maze[p[0]][p[1]], p)


def init_labyrinthe():
    """
    Point de départ du labyrinthe
    """
    return [1, 1]


def est_final_labyrinthe(s):
    """
    Permet de savoir si on est arrivé sur la cellule finale
    """
    return s == [10, 11]


def decision_labyrinthe():
    """ """
    a = choice(actions_labyrinthe())
    return a


def boltzmann(Q, actions, s, to):
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
        ex = math.exp((Q[s[1]][s[0]][action]) / to)
        v = 0
        for a in actions:
            v += math.exp((Q[s[1]][s[0]][a]) / to)
        p = ex / v
        l.append(p)

    return l


def gloutonne(Q, actions, s, a):
    """
    Fonction pour le modèle glouton

    Parameters
    ----------
    Q : TYPE
        DESCRIPTION.
    actions : TYPE
        DESCRIPTION.
    s : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    l = list()
    for action in actions:
        l.append((Q[s[1]][s[0]][action], action))

    p = list(v[0] for v in l)

    for elt in p:
        if elt != 0:
            return max(l, key=lambda x: x[0])[1]
    return choice(actions)


def teleportation(maze, final, episode):
    """
    fonction qui renvoi le labyrinthe passé en paramètre mais en déplacent l'état final en le téléportant.
    Un épisode sur 2 il va se téléporter de la case (6,3) à la (3,6)
    """
    if episode % 2 == 0:
        coo = [10, 4]
        maze[coo[0]][coo[1]], maze[final[0]][final[1]] = (
            maze[final[0]][final[1]],
            maze[coo[0]][coo[1]],
        )
        return coo
    else:
        coo = [7, 3]
        maze[coo[0]][coo[1]], maze[final[0]][final[1]] = (
            maze[final[0]][final[1]],
            maze[coo[0]][coo[1]],
        )

        return coo


##########################################################################################


def Q_Learning(etats, actions, gamma, execution, init, decision, final, environnement):
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
    # Q va nous permettre de stocker la qualité pour tous les couples (etat , action) sous forme de matrice
    ligne = len(environnement)
    colonne = len(environnement[0])

    Q = list()
    for i in range(ligne):
        jl = list()
        for j in range(colonne):
            kl = list()
            for k in range(len(actions)):
                kl.append(0)
            jl.append(kl)
        Q.append(jl)

    laa = list()
    acc = list()
    cpt = 0
    x = list()
    y = list()

    # N va nous permettre de calculer le taux d'apprentissage pour  chaque
    N = list()
    for i in range(ligne):
        jl = list()
        for j in range(colonne):
            kl = list()
            for k in range(len(actions)):
                kl.append(0)
            jl.append(kl)
        N.append(jl)

    while cpt < 70:  # On va faire 70 épisodes
        s = list()
        s.append(init())
        ac = list()
        t = 0
        r = list()
        a = list()
        la = list()
        ct = 0

        while not final(s[t]):  # On va faire 1 épisode
            actionsPossibles = list()
            for ap in actions:
                if execution(s[t], ap)[0] != -100:
                    actionsPossibles.append(ap)

            d = decision(
                Q, actionsPossibles, s[t], 1
            )  # A utiliser si on veut utiliser la manière Boltzmann
            action = choices(actionsPossibles, d, k=1)[
                0
            ]  # A utiliser si on veut utiliser la manière Boltzmann

            # action = decision(Q , actionsPossibles , s[t] , 1 ) #A utiliser si on veut utiliser la manière gloutonne

            a.append(execution(s[t], action))

            r.append(a[t][0])  # le retour rt
            s.append(a[t][1])  # L'état st+1

            la.append(action)

            alpha = 1 / (1 + N[s[t][1]][s[t][0]][action])

            l = list()
            for ac in actions:
                l.append(Q[s[t + 1][1]][s[t + 1][0]][ac])
            v = max(l)

            Q[s[t][1]][s[t][0]][action] = Q[s[t][1]][s[t][0]][action] + alpha * (
                r[t] + gamma * v - Q[s[t][1]][s[t][0]][action]
            )

            N[s[t][1]][s[t][0]][action] += 0.01

            ct += 1

            t += 1

        acc.append(ac)
        laa.append(la)

        cpt += 1

        y.append(len(la))
        x.append(cpt)

    print(
        len(laa[-1])
    )  # Cela va nous permettre de connaitre le nombre de pas fait pour le dernier épisode
    return x, y, Q


#########################################------GRAPHIQUE------#####################################################


# Ici on va récolter les données de 15 appel à la fonction pour ensuite en faire un graphique
data = list()
for i in range(15):
    v = Q_Learning(
        etats_labyrinthe(),
        actions_labyrinthe(),
        0.9,
        exectution_labyrinthe,
        init_labyrinthe,
        boltzmann,
        est_final_labyrinthe,
        maze,
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
"""
import seaborn as sns; sns.set_theme()

QModifier = Q_Learning(etats_labyrinthe() , actions_labyrinthe() , 0.9 , exectution_labyrinthe , init_labyrinthe , boltzmann  , est_final_labyrinthe , maze)[2]


il = list()
for i in range(16):
    jl = list()
    for j in range(16):
        jl.append(max(QModifier[j][i]))
    il.append(jl)



    
uniform_data = il
ax = sns.heatmap(uniform_data)
"""
####################################################################################################################


CSI = "\x1B["


def affichage(maze, s):
    global t
    t = tuple()
    ligne = len(maze)
    colonne = len(maze[0])
    for i in range(ligne):
        for j in range(colonne):
            if i == s[0] and j == s[1]:
                print(CSI + "30;40m" + " A" + CSI + "0m", end="")
            elif maze[i][j] == -100:
                print(CSI + "31;41m" + " W" + CSI + "0m", end="")
            elif maze[i][j] == 0:
                print(CSI + "37;47m" + " P" + CSI + "0m", end="")
            elif maze[i][j] == 100:
                print(CSI + "34;44m" + " S" + CSI + "0m", end="")
            else:
                print(CSI + "32;42m" + " D" + CSI + "0m", end="")
        print("")


CSI = "\x1B["


def affichage2_0(maze, s, final):
    ligne = len(maze)
    colonne = len(maze[0])
    for i in range(ligne):
        for j in range(colonne):
            if i == s[0] and j == s[1]:
                print(CSI + "30;40m" + " A" + CSI + "0m", end="")

            # elif(final[0]==i and final[1]==j):
            #  print(CSI+"34;44m" + " S" + CSI + "0m" , end='')

            elif maze[i][j] == -100:
                print(CSI + "31;41m" + " W" + CSI + "0m", end="")
            elif maze[i][j] == 0:
                print(CSI + "37;47m" + " P" + CSI + "0m", end="")

            elif maze[i][j] == 100:
                print(CSI + "34;44m" + " S" + CSI + "0m", end="")

            else:
                print(CSI + "32;42m" + " D" + CSI + "0m", end="")
        print("")


file = open("Maze1.txt", "r")  # Ici on va ouvrir le petit labyrinthe

maze = list()
for line in file:
    l = list()
    for character in line:
        if character != "\n":
            l.append(conversion(character))
    maze.append(l)

maze.reverse()


def deplacement1(maze, final, episode):
    """
    fonction qui renvoi le labyrinthe passé en paramètre mais en déplacent l'état final.
    Un épisode sur 2 il va se déplacer de 1 vers la gauche, sinon vers la droite
    """
    if episode % 2 == 0:
        coo = exectution_labyrinthe(final, 2)[1]
        maze[coo[0]][coo[1]], maze[final[0]][final[1]] = (
            maze[final[0]][final[1]],
            maze[coo[0]][coo[1]],
        )
        return coo
    else:
        coo = exectution_labyrinthe(final, 0)[1]
        maze[coo[0]][coo[1]], maze[final[0]][final[1]] = (
            maze[final[0]][final[1]],
            maze[coo[0]][coo[1]],
        )
        return coo


def deplacement2(maze, final, episode):
    """
    fonction qui renvoi le labyrinthe passé en paramètre mais en déplacent l'état final en le téléportant.
    Un épisode sur 2 il va se téléporter de la case (6,3) à la (3,6)
    """
    if episode % 2 == 0:
        coo = [3, 6]
        maze[coo[0]][coo[1]], maze[final[0]][final[1]] = (
            maze[final[0]][final[1]],
            maze[coo[0]][coo[1]],
        )
        return coo
    else:
        coo = [6, 3]
        maze[coo[0]][coo[1]], maze[final[0]][final[1]] = (
            maze[final[0]][final[1]],
            maze[coo[0]][coo[1]],
        )
        return coo


# Cette fonction sert seulement à l'affichage pour le petit labyrinthe (ajout de la fonction affichage dans le code)
def Q_Learning_PourAffichage(
    etats, actions, gamma, execution, init, decision, final, environnement
):
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
    ligne = len(environnement)
    colonne = len(environnement[0])

    # Q va nous permettre de stocker la qualité pour tous les couples (etat , action)

    Q = list()
    for i in range(ligne):
        jl = list()
        for j in range(colonne):
            kl = list()
            for k in range(len(actions)):
                kl.append(0)
            jl.append(kl)
        Q.append(jl)

    # N va nous permettre de calculer le taux d'apprentissage pour  chaque
    N = list()
    for i in range(ligne):
        jl = list()
        for j in range(colonne):
            kl = list()
            for k in range(len(actions)):
                kl.append(0)
            jl.append(kl)
        N.append(jl)
    laa = list()
    acc = list()
    cpt = 0
    x = list()
    y = list()
    final = [6, 3]

    while cpt < 20:  # On va faire 70 épisodes
        s = list()
        s.append([1, 2])
        ac = list()
        t = 0
        r = list()
        a = list()
        la = list()
        ct = 0
        val = time.perf_counter()

        # final = deplacement2(maze , final , cpt)

        while s[t] != final:
            print(s[t], final)
            print("Episode : " + str(cpt))
            print("Action : " + str(ct))
            while time.perf_counter() - val < 0.1:
                pass

            val = time.perf_counter()

            actionsPossibles = list()
            for ap in actions:
                if execution(s[t], ap)[0] != -100:
                    actionsPossibles.append(ap)

            d = decision(Q, actionsPossibles, s[t], 1)  # Cas Boltzmann
            action = choices(actionsPossibles, d, k=1)[0]

            # action = decision(Q , actionsPossibles , s[t] , 1 ) #Cas glouton

            a.append(execution(s[t], action))
            r.append(a[t][0])  # le retour rt
            s.append(a[t][1])  # L'état st+1

            la.append(action)
            alpha = 1 / (1 + N[s[t][1]][s[t][0]][action])

            l = list()
            for ac in actions:
                l.append(Q[s[t + 1][1]][s[t + 1][0]][ac])
            v = max(l)

            Q[s[t][1]][s[t][0]][action] = Q[s[t][1]][s[t][0]][action] + alpha * (
                r[t] + gamma * v - Q[s[t][1]][s[t][0]][action]
            )

            ct += 1

            t += 1
            p = s
            p[0], p[1] = p[1], p[0]
            affichage2_0(maze, s[t], final)

            print("---------------------------------------------")

        acc.append(ac)
        laa.append(la)
        cpt += 1

        y.append(len(la))
        x.append(cpt)
    return x, y


"""

Q_Learning_PourAffichage(etats_labyrinthe() , actions_labyrinthe() , 0.9 , exectution_labyrinthe , init_labyrinthe , boltzmann ,est_final_labyrinthe , maze)
"""
