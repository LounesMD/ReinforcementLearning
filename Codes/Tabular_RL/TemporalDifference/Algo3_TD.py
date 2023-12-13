# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 17:46:18 2021

@author: Lounès

Value Function based algorithm.

This file gives an implementation of the TD algorithm that computes the Value Function from a given policy.

The main difference with the previous algorithms is that we DO NOT know both the reward function and the transition function
"""

from random import choice, choices

import matplotlib.pyplot as plt


def actions():
    actions = [0, 1, 2]
    return actions


def etats():
    etats = [0, 1, 2]
    return etats


def etat_suivant(etat, action):
    """
    Cette fonction nous permet de savoir où on va pouvoir aller après avoir fait une action

    Parameters
    ----------
    etat : int
        état actuel.
    action : int
        action fait.

    Returns
    -------
    list
        renvoie une liste qui est composée d'un tuple (retour,proba,etat de ce choix) .

    """
    l = [  # Ensemble d'arrivé en partant de l'état A
        [
            [(10, 1 / 2, 0), (4, 1 / 4, 1), (8, 1 / 4, 2)],
            [(8, 1 / 16, 0), (2, 3 / 4, 1), (4, 3 / 16, 2)],
            [(4, 1 / 4, 0), (6, 1 / 8, 1), (4, 5 / 8, 2)],
        ],
        [  # Ensemble d'arrivé en partant de l'état B
            [(14, 1 / 2, 0), (0, 0, 1), (18, 1 / 2, 2)],
            0,
            [(8, 1 / 16, 0), (16, 7 / 8, 1), (8, 1 / 16, 2)],
        ],
        [  # Ensemble d'arrivé en partant de l'état C
            [(10, 1 / 4, 0), (2, 1 / 4, 1), (8, 1 / 2, 2)],
            [(6, 1 / 8, 0), (4, 3 / 4, 1), (2, 1 / 8, 2)],
            [(4, 3 / 4, 0), (0, 1 / 16, 1), (8, 3 / 16, 2)],
        ],
    ]
    return l[etat][action]


def politique_taxi():
    """
    Le but avec cette politique est de s'approcher des valeurs qu'on a eu avant.
    Donc cela revient à faire l'action A->a2 B->a3 C->a2

    Returns
    -------
    list
        politique pour chaque état.

    """
    return [1, 2, 1]


def init():
    return choice(etats())


def est_final(t):
    """
    Fonction qui permet de savoir si l'état t passé en paramètre est l'état final ou non.
    Cette fonction est utilisée pour illustrer l'exemple du taxi, on va donc estimer qu'on est dans un état final
    après être passé dans 20 états après l'état initial avant d'arrêter

    Parameters
    ----------
    t : int
        entier qui correspond à l'état.

    Returns
    -------
    bool
        True si on est dans l'état final, false si non.

    """
    est_final.counter += 1
    if est_final.counter > 300:
        est_final.counter = 0
        return True
    else:
        return False


est_final.counter = 0


def td(etats, actions, gamma, politique, init, est_final, etat_suivant):
    """
    Parameters
    ----------
    etats : list
        liste des états possibles
    actions : int
        Entier qui correspond aux nombre d'actions possibles.
    gamma : int
        facteur déprécié.
    politique : list
        Matrice(n,m) qui correspond à la politique où n représente un état et m la proba d'arriver dans un état après une actions

    Returns
    -------
    list
        renvoie la liste des valeurs de cet environnement.

    """
    # On commence par initialiser la fonction valeur et le % taux d'apprentissage %
    VS = list()
    for i in range(len(etats)):
        VS.append(0)

    NS = list()
    for i in range(len(etats)):
        NS.append(0)

    cpt = 0

    while (
        cpt < 100000
    ):  # Le problème ici, c'est qu'il faut vérifier les conditions (càd : passer une infinité de fois dans chaque état )
        t = 0
        s = list()  # On va stocker tous les états
        s.append(init())
        r = list()  # On va stocker toutes les retours
        a = list()  # Et également toutes les actions
        while not est_final(s[t]):  # On vérifie le critère de l'état final
            # Faire l'action
            # Pour l'action, on va utiliser la politique, qui va nous donner un état d'arriver et un retour rt

            print(
                "on est dans l'état "
                + str(s[t])
                + " et on fait l'action "
                + str(politique[s[t]])
            )
            a.append(
                politique[s[t]]
            )  # De là, on va pouvoir observer un retour et un nouvel état (car l'action va nous le permettre)

            # Observer rt et st+1:
            l = etat_suivant(
                s[t], a[t]
            )  # Là, on connait notre état actuel + l'action qu'on doit faire, pour cela on récupère l'ensemble des possibilités
            p = choices(l, list(i[1] for i in l))[
                0
            ]  # On fait un choix aléatoire parmi  les états suivant possibles (en fonction de leur probabilité)
            print(l, p)
            r.append(p[0])  # une foix choisi, on observe un retour rt
            s.append(p[2])  # ainsi qu'un nouvel état st+1

            alpha = 1 / (1 + NS[s[t]])

            VS[s[t]] = VS[s[t]] + alpha * (r[t] + gamma * VS[s[t + 1]] - VS[s[t]])

            NS[s[t]] = NS[s[t]] + 1
            t += 1

        cpt += 1
        print(cpt, VS)
    return VS


print("---------------Algorithme3 : TEST-----------------")


valeur = td(etats(), actions(), 0.9, politique_taxi(), init, est_final, etat_suivant)
print(valeur)
