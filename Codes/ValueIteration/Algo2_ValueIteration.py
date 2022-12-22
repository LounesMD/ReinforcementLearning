# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 09:21:18 2021

@author: Lounès

Value Function based algorithm.

This file gives an implementation of an algorithm that computes a policy from the optimal Value function.
For this purpose we 
1) Compute the optimal Value Function using the Bellman optimal equation
2) Compute the policy by choosing the action that gives the best value from a state

"""

from Algo0_ValueFunction import valeur
from Algo0_ValueFunction import transition_taxi
from Algo0_ValueFunction import retour_taxi


def IterationValeur(etats , actions , transitions , retour , gamma , epsilon):
    """
    
    Fonction qui permet d'avoir la valeur optimale par itération sur les valeurs
    
    Parameters
    ----------
    etats : lsit
        liste des etats utilisables.
    actions : list
        liste des actions.
    transitions : dict
         dictionnaire qui associe à chaque état ces actions possibles et qui associe également à chaque action la probabilité d'arriver dans un auter état.
    retour : dict
         dictionnaire qui associe à chaque état ces actions possibles et qui associe également à chaque action le retour associé à chaque état d'arrivé.
    gamma : int
        facteur déprécié.
    epsilon : int
        Seuil de précision.

    Returns
    -------
    dict qui associe à chaque état sa valeur pour une politique optimale.

    """

    ValeurK = dict()
    for etat in etats:
        ValeurK[etat] = 0
        
        
    ValeurK1 = dict()
    for etat in etats:
        ValeurK1[etat] = 0
    
    #1ère boucle
    cmp = epsilon*((1 - gamma)/(2*gamma)) +1

    while cmp >  epsilon*((1 - gamma)/(2*gamma)) :

        #On va stocker dans VK+1 la valeur de chaque état
        for etat in etats:
            l = list()
            actionsPossibles = transitions[etat].keys()
            for action in actionsPossibles:
                v=0
                for etatp in etats:
                    v+=(transitions[etat][action][etatp]) * (retour[etat][action][etatp] + gamma * ValeurK[etatp])
                l.append(v)
                
            ValeurK1[etat] = max(l)
            l=[]

        #On va stocker la différence ||Vk+1-Vk||infinie dans cmp 
        l = list()
        for etat in etats: 
            l.append(abs(ValeurK1[etat]-ValeurK[etat]))
        cmp = max(l)
        
        #On passe à l'incrémentation
        ValeurK = ValeurK1.copy()

    #2ème boucle
    politique = dict()
    for etatp in etats:
        politique[etatp] = None

    for etatp in etats:
        actionsPossibles = transitions[etatp].keys()
        l = list()
        for action in actionsPossibles:
            v = 0
            for j in etats:
                v+=transitions[etatp][action][j] * (retour[etatp][action][j] + gamma * ValeurK[j])
            l.append([action,v])      
        politique[etatp] = max(l, key=lambda x:x[1])[0]
    
    return [politique,ValeurK]     
    
    
print("---------------Algorithme2 : TEST-----------------")
actions = list()
actions.append('a1')
actions.append('a2')
actions.append('a3')


etats = list()
etats.append('A')
etats.append('B')
etats.append('C')

politique = IterationValeur(etats , actions , transition_taxi() , retour_taxi() , 0.9 , 0.01)
print("Avec l'algotithme d'itération sur les valeurs, on trouve comme valeur optimale pour chaque état :")
print(politique[1])
print("Et ça avec la politique : ")
print(politique[0])












