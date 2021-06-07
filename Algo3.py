# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 17:46:18 2021

@author: Lounès
"""

from random import choices
from random import choice

def actions():
    actions = [0,1,2]
    return actions
    
def etats():
    etats = [0,1,2]
    return etats

def etat_suivant( etat , action ):
    l =[[ [(10,1/2,0),(4,1/4,1),(8,1/4,2)] ,  [(8,1/16,0),(2,3/4,1),(4,3/16,2)] , [(4,1/4,0),(6,1/8,1),(4,5/8,2)] ],[ [(14,1/2,0),(0,0,1),(18,1/2,2)] , 0 , [(8,1/16,0),(16,7/8,1),(8,1/16,2)] ],[ [(10,1/4,0),(2,1/4,1),(8,1/2,2)] , [(6,1/8,0),(4,3/4,1),(2,1/8,2)] , [(4,3/4,0),(0,1/16,1),(8,3/16,2)]  ]]
    return l[etat][action]



def politique_taxi():
    return  [1 , 2 , 1]

    
def init():
    return choice(etats())



def est_final(t):
    est_final.counter += 1
    if(est_final.counter>20):
        est_final.counter = 0
        return True
    else:
        return False

est_final.counter = 0
    
    
    


def td(etats , actions , gamma , politique , init , est_final , etat_suivant ):
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
    None.

    """
    #On commence par initialiser la fonction valeur et le % taux d'apprentissage %
    VS = list()
    for i in range(len(etats)):
        VS.append(0)
        
    NS = list()
    for i in range(len(etats)):
        NS.append(0)
        
    cpt = 0
    
    #On va stocker toutes les actions faites, les états passés, les retours gagnés
 
    #On va faire 10000 épisodes
    while cpt < 10000: #Le problème ici, c'est qu'il faut vérifier les conditions 
        t = 0
        s = list()
        s.append(init())
        r = list()
        a = list()
        while( not est_final(s[t]) ): 
            #Faire l'action 
            #Pour l'action, on va utiliser la politique, qui va nous donner un état d'arriver et un retour rt
            a.append(politique[s[t]])   #De là, on est censé pouvoir observer un retour et un nouvel état (car l'action va nous le permettre)                             
            #Observer rt et st1        
                        
            l = etat_suivant(s[t],a[t]) #Là, on connait notre état actuel + l'action qu'on doit faire, pour cela on récupère l'ensemble des possibilités 
            p = choices(l , list(i[1] for i in l ) )[0] #On fait un choix aléatoire parmi de l'état suivant (en fonction de leur probabilité)
            r.append(p[0]) #une foix choisi, on observe un retour
            s.append(p[2])#ainsi qu'un nouvel état

            alpha= 1/(1+NS[s[t]])
            VS[s[t]] = VS[s[t]] + alpha * (r[t] + gamma*VS[s[t+1]] - VS[s[t]] )
            
            NS[s[t]] = NS[s[t]] + 1
            t+=1                    
        cpt+=1

    return VS
        

print("---------------Algorithme3 : TEST-----------------")

    
        
valeur = td(etats() , actions() , 0.9 , politique_taxi() , init , est_final ,etat_suivant )
print(valeur)