# -*- coding: utf-8 -*-
"""
Created on Mon May 31 10:56:43 2021

@author: Lounès
"""

import matplotlib.pyplot as plt


def politique_taxi():
    """
    Politique pour l'exemple du taxi
    """
    politique = dict()
    politique['A'] = {'a1':0 , 'a2':1 , 'a3':0}
    politique['B'] = {'a1':0 , 'a3':1}
    politique['C'] = {'a1':0 , 'a2':1 , 'a3':0}
    return politique



def transition_taxi():
    """
    Fonction de transition pour l'exemple du taxi
    """
    transi_retour = dict()
    transi_retour['A'] = {'a1':{'A':1/2 , 'B':1/4 , 'C':1/4} , 
                          'a2':{'A':1/16 , 'B':3/4 , 'C':3/16} , 
                          'a3':{'A':1/4 , 'B':1/8 , 'C':5/8}
                          }
    
    transi_retour['B'] = {'a1':{'A':1/2 , 'B':0 , 'C':1/2} , 
                          #'a2':{'A':0  , 'B':0  , 'C':0 } , 
                          'a3':{'A':1/16 , 'B':7/8 , 'C':1/16}
                          }
    
    transi_retour['C'] = {'a1':{'A':1/4 , 'B':1/4 , 'C':1/2} , 
                          'a2':{'A':1/8 , 'B':3/4 , 'C':1/8} , 
                          'a3':{'A':3/4 , 'B':1/16 , 'C':3/16}
                          }
    
    return transi_retour

def retour_taxi():
    """
    Fonction de retour pour l'exemple du taxi
    """
    transi_retour = dict()
    transi_retour['A'] = {'a1':{'A':10 , 'B':4 , 'C':8} , 
                          'a2':{'A':8  , 'B':2 , 'C':4} , 
                          'a3':{'A':4  , 'B':6 , 'C':4}
                          }
    
    transi_retour['B'] = {'a1':{'A':14 , 'B':0 , 'C':18} , 
                          #'a2':{'A':0  , 'B':0 , 'C':0} , 
                          'a3':{'A':8  , 'B':16 , 'C':8}
                          }
    
    transi_retour['C'] = {'a1':{'A':10 , 'B':2 , 'C':8} , 
                          'a2':{'A':6  , 'B':4 , 'C':2} , 
                          'a3':{'A':4  , 'B':0 , 'C':8}
                          }
    
    return transi_retour

        
def valeur(politique,actions,etats,transitions,retour,gamma):
    """
    Renvoie la valeur associée à la politique donnée pour un certain état initial
    
    CU:
        
    :param politique: politique de l'environnement
    :param actions: liste des actions possibles à partir de tous les états
    :param etats: état possible dans l'environnement
    :param transitions:fonction de transition (qui renvoie la proba à partir de l'état s en faisant l'action a d'arriver à l'état s' )
    :param retour:fonction de retour (qui renvoie le retour à partir de l'état s en faisant l'action a pour arriver à l'état s' )
    :param gamme: gamma 
    
    :return: Valeur de cet environnement pour la politique donnée
        
    
    """
    cp = 1

    #On commence par initialiser tous les Vk(s) à 0     
    ValeurK = dict()
    for e in etats:
        ValeurK[e]=0
 
    #On va donc utiliser un dictionnaire Vk+1 qui commence aussi à 0
    ValeurK1 = ValeurK.copy()

    #Tant que l'écart entre Vk et Vk+1 est inférieur à ???
    while(cp > 0.00001 ):     
        
        for etat in etats:
            
            #Somme des politiques (Première somme dans la définition)              
            Sactions = 0
            actionsPossibles = transitions[etat]
            for action in actionsPossibles:         
                #On va récupérer la valeur de la politique associée à cet état pour l'action action
                v1=politique[etat][action]
    
                #On va maintenant la somme pour tous les états (calculer la deuxième somme de la définition)
                Setats = 0            
                
                for j in  etats:
                    Setats+= transitions[etat][action][j]*(retour[etat][action][j]+gamma*ValeurK[j])   
                #On fait donc le produit de v1 et Setats
                v2=v1*Setats
                
    
                #On on l'ajoute à Sactions qui est la 1ère somme dans la définition
                Sactions += v2
                
            #On stock dans Vk+1(etat) la valeur calculée
            ValeurK1[etat] = Sactions
        #On va stocker la différence ||Vk+1-Vk||infinie 
        l = list()
        for etat in etats:
            l.append(ValeurK1[etat]-ValeurK[etat])
        cp = max(l)
        
        #Puis on incrémente, càd que Vk prend la valeur Vk+1 et Vk+1 devient Vk+2 qui est la nouvelle valeur à chercher
        ValeurK = ValeurK1.copy()
    #A la fin ,nous avons la meilleur valeur possible
    return ValeurK


print("---------------Algorithme 0 : TAXI-----------------")
actions = list()
actions.append('a1')
actions.append('a2')
actions.append('a3')


etats = list()
etats.append('A')
etats.append('B')
etats.append('C')

        
V = valeur(politique_taxi() , actions , etats , transition_taxi(),retour_taxi() , 0.9)
print(V)

politique = dict()
politique['A'] = {'a1':0 , 'a2':0 , 'a3':0}
politique['B'] = {'a1':0 , 'a3':0}
politique['C'] = {'a1':0 , 'a2':0 , 'a3':0}

"""
y = list()
for i in ['a1','a2','a3']:
    politique['A'][i] = 1
    for j in ['a1','a3']:
        politique['B'][j] = 1
        for k in ['a1','a2','a3']:
            politique['C'][k] = 1
            p = valeur(politique , actions , etats , transition_taxi(),retour_taxi() , 0.9) 
            y.append(list(p[i] for i in p))
            politique['C'][k] = 0
        politique['B'][j]=0
    politique['A'][i] = 0
            
print(y)

x = ['A','B','C']


for yy in y:
    plt.plot(x, yy, color='black', linestyle='dashed', linewidth = 1,
         marker='x', markerfacecolor='black', markersize=5)

plt.xlabel('x - états')

plt.ylabel('y - valeurs')
  
plt.title('fonction valeur de toutes les politiques')

plt.show()
"""