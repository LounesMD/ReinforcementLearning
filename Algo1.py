# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 13:28:06 2021

@author: Lounès
"""
import random
from random import choice
from random import random
from Algo0 import transition_taxi
from Algo0 import retour_taxi


def random_pol(actions):
    """
    Fonction qui nous permet d'avoir une politique aléatoire en fonction des actions possible
 
  
    :param actions: liste des actions pouvant être éffectuées dans notre environnement.

    :return: action        
    """

    return choice(actions)




def IterationPolitiques(etats , actions , transitions , retour , gamma , epsilon ):
    """
    Renvoie la politique epsilon-optimale par la méthode par itération sur les politiques
    
    CU:
        
    :param actions: liste des actions possibles à partir de l'état debut 
    :param etats: état possible dans l'environnement
    :param transitions:fonction de transition (qui renvoie la proba à partir de l'état s en faisant l'action a d'arriver à l'état s' )
    :param retour:fonction de retour (qui renvoie le retour à partir de l'état s en faisant l'action a pour arriver à l'état s' )
    :param gamma: gamma 
    
    :return: politique epsilon-optimale
    """
    politique = dict();    
    #On génère une politique initiale aléatoire
    for etat in etats:
        actionsPossibles = list(transitions[etat])
        politique[etat] = random_pol(actionsPossibles)

    politique_bis = dict();
    
    #On génère une politique_bis pour passer la 1ère vérification 
    for etat in etats:
        politique_bis[etat] = None

    comp = politique != politique_bis
    
    while(comp):      
        #On commence par initialiser tous les Vi(s) à une valeur aléatoire         
        ValeurI = dict()
        for e in etats:
            ValeurI[e]=random()
 
        #On va donc utiliser un dictionnaire VI+1 pour chercher la politique epsilon-optimale
        ValeurI1 = dict()
    
        cmp = epsilon*((1 - gamma)/(2*gamma)) +1
        
        #1ère boucle
        while cmp > epsilon*((1 - gamma)/(2*gamma)) :
            #On va stocker dans VI+1 la valeur de chaque état
            for etat in etats:
                v=0
                for etatp in etats:
                    v += (transitions[etat][politique[etat]][etatp]) * (retour[etat][politique[etat]][etatp] + gamma * ValeurI[etatp])
                ValeurI1[etat] = v

            #On va stocker la différence ||Vk+1-Vk||infinie dans cmp 
            l = list()
            for etat in etats: 
                l.append(ValeurI1[etat]-ValeurI[etat])
            cmp = max(l)

            ValeurI = ValeurI1.copy()

        #2ème boucle
        for etat in etats:

            l= []
            actionsPossibles = transitions[etat].keys()
            for action in  actionsPossibles:
                v=0                
                for etatp in etats:
                    v+= transitions[etat][action][etatp] * (retour[etat][action][etatp] + gamma*ValeurI[etatp])                    
                l.append([action,v])
            politique_bis[etat] = max(l, key=lambda x:x[1])[0]

            
        comp = politique != politique_bis
        politique = politique_bis.copy()
        
    return [politique,ValeurI]



print("---------------Algorithme1 : TEST-----------------")
actions = list()
actions.append('a1')
actions.append('a2')
actions.append('a3')


etats = list()
etats.append('A')
etats.append('B')
etats.append('C')

politique = IterationPolitiques(etats , actions , transition_taxi() , retour_taxi() , 0.9 , 0.01)
print("Avec l'algotithme d'itération sur les politiques, on trouve comme valeur optimale pour chaque état :")
print(politique[1])
print("Et ça avec la politique : ")
print(politique[0])


