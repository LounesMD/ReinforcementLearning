# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 11:03:04 2021

@author: Lounès

Algortithme de Q-learning
"""
import time
from random import choice
from random import choices
import math
import matplotlib.pyplot as plt
import numpy as np



"""
CE FICHIER EST L'IMPLEMENTATION DE LA PARTIE 3.5.5.1 càd la partie qui étudie le comportement de la learning 
pour une fonction qualité déjà entrainée.
"""




#####################################Fonctions utiles#####################################
def conversion(c):
    """
    Fonction qui permet de convertir le caractère c en un certain nombre
    """
    if(c=='*'):
        return -100
    elif(c ==' '):
        return 0
    elif(c=='O'):
        return -1
    elif(c=='V'):
        return 100



file = open("Maze.txt","r")

maze = list()
for line in file:
    l = list()
    for character in line:
        if(character != '\n'):
            l.append(conversion(character))
    maze.append(l)
    
maze.reverse() #Ce la va nous permettre d'avoir le (0,0) en bas à gauche de notre labyrinthe




def etats_labyrinthe():
    """
    On va définir tous les états possibles du labyrinthe. Ce qui correspond aux coordonnées du plateau
    """
    l = list()
    for i in range(16):
        for j in range(16):
            l.append([i,j])
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
    return [0,1,2,3]

def exectution_labyrinthe(etat,action):
    """
    fonction qui va permettre d'executer l'action passer en paramètre dans l'environnement du labyrinthe et renvoyer:
        (retour , etat) qui sont les choses à observer une fois l'action effectuée
    """
    p=etat.copy()
    if(action==0):
        if(p[1]+1 > len(maze[0]) - 1):
            return ( maze[p[0]][p[1]] , p )
        p[1]+=1
        return ( maze[p[0]][p[1]] , p )
    if(action==1):
        if(p[0]+1 > len(maze) -1 ):   
            return ( maze[p[0]][p[1]] , p )
        p[0]+=1
        return ( maze[p[0]][p[1]] , p )
    if(action==2):
        if(p[1]-1 < 0):
            return ( maze[p[0]][p[1]] , p )
        p[1]-=1
        return ( maze[p[0]][p[1]] , p )
    if(action==3):
        if(p[0]-1 < 0):
            return ( maze[p[0]][p[1]] , p )
        p[0]-=1
        return ( maze[p[0]][p[1]] , p )


def init_labyrinthe():
    """
    Point de départ du labyrinthe
    """
    return [1,1]

def est_final_labyrinthe(s):
    """
    Permet de savoir si on est arrivé sur la cellule finale
    """
    return s == [10,11]
    #return s == [14,4]

def decision_labyrinthe():
    """
    """
    a = choice(actions_labyrinthe())
    return a



def boltzmann(Q , actions , s , to):  
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
    l =  list()
    for action in actions:
        p = 0     
        ex = math.exp((Q[s[1]][s[0]][action])/to)        
        v = 0        
        for a in actions:     
            v+= math.exp((Q[s[1]][s[0]][a])/to)        
        p = ex / v
        l.append(p)
    return l
    

def gloutonne(Q , actions , s , a):
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
        l.append( ( Q[s[1]][s[0]][action] ,action) )
    
    p = list(v[0] for v in l )
    
    for elt in p:
        if(elt != 0):
            return max(l , key=lambda x:x[0] )[1]
    return choice(actions)
    

def teleportation(maze , final , episode):
    """
    fonction qui renvoi le labyrinthe passé en paramètre mais en déplacent l'état final en le téléportant.
    Un épisode sur 2 il va se téléporter de la case (6,3) à la (3,6)
    """    
    if episode%2 == 0:
        coo =  [10,11]
        maze[coo[0]][coo[1]] , maze[final[0]][final[1]] =   maze[final[0]][final[1]] ,  maze[coo[0]][coo[1]]
        return coo
    else:
        coo = [7,3]
        maze[coo[0]][coo[1]] , maze[final[0]][final[1]] =   maze[final[0]][final[1]] ,  maze[coo[0]][coo[1]]

        return coo



    

    
CSI="\x1B["
def affichage2_0(maze , s , final):    
    print(final)
    ligne = len(maze)
    colonne =  len(maze[0])
    for i in range(ligne):
        for j in range(colonne):
            if(i == s[0] and j ==s[1]):
                print (CSI+"30;40m" + " A" + CSI + "0m" , end='')
                
            #elif(final[0]==i and final[1]==j):
             #  print(CSI+"34;44m" + " S" + CSI + "0m" , end='')
                
            elif(maze[i][j] == -100 ):                
                print(CSI+"31;41m" +' W' + CSI + "0m" , end='')
            elif(maze[i][j]==0):
                print(CSI+"37;47m" + " P" + CSI + "0m" , end='')
            
            elif(maze[i][j]==100):
                print(CSI+"34;44m" + " S" + CSI + "0m" , end='')

            else:
                print(CSI+"32;42m" + " D" + CSI + "0m",end='')
        print('')
        
        
        
def teleporteSpawn(maze , spawn , episode):
    """
    Fonction qui permet de faire changer l'état initial

    Parameters
    ----------
    maze : TYPE
        DESCRIPTION.
    spawn : TYPE
        DESCRIPTION.
    episode : TYPE
        DESCRIPTION.

    Returns
    -------
    coo : TYPE
        coordonnée du nouvel état initial.

    """
    if episode%4 == 0:
        coo =  [10,1]
        maze[coo[0]][coo[1]] , maze[spawn[0]][spawn[1]] =   maze[spawn[0]][spawn[1]] ,  maze[coo[0]][coo[1]]
        return coo
    elif episode%3 == 0:
        coo =  [12,11]
        maze[coo[0]][coo[1]] , maze[spawn[0]][spawn[1]] =   maze[spawn[0]][spawn[1]] ,  maze[coo[0]][coo[1]]
        return coo
    if episode%2 == 0:
        coo =  [1,13]
        maze[coo[0]][coo[1]] , maze[spawn[0]][spawn[1]] =   maze[spawn[0]][spawn[1]] ,  maze[coo[0]][coo[1]]
        return coo
    else:
        coo = [1,1]
        maze[coo[0]][coo[1]] , maze[spawn[0]][spawn[1]] =   maze[spawn[0]][spawn[1]] ,  maze[coo[0]][coo[1]]
        return coo
########################################################################################## 
   










     
def Q_Learning(Q , etats , actions , gamma , execution , init , decision , final , environnement):
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
    #Q va nous permettre de stocker la qualité pour tous les couples (etat , action) sous forme de matrice
    ligne = len(environnement)
    colonne =  len(environnement[0])
    
    Q = Q

    
    #N va nous permettre de calculer le taux d'apprentissage pour  chaque 
    N = list()
    for i in range(ligne):
        jl= list()
        for j in range(colonne):
            kl= list()
            for k in range(len(actions)):
                kl.append(0)
            jl.append(kl)
        N.append(jl)
   
    #N va nous permettre de calculer le taux d'apprentissage pour  chaque 
    P = list()
    for i in range(ligne):
        jl= list()
        for j in range(colonne):
            jl.append(0)
        P.append(jl)
    
        
   
    
    laa = list()
    acc = list()
    cpt = 0
    x = list()
    y = list()
    while(cpt < 70 ): #On va faire 70 épisodes
    
        s = list()        
        s.append( init() ) #A utiliser si on veut utiliser l'état initial de base
        #s.append([x,y]) Si on veut changer de place l'état initial
        ac = list()
        t=0
        r = list()
        a = list()
        la = list()
        ct = 0    
        
        while not final(s[t])  : #Si on veut changer l'état final, il faut aller le modifier dans la fonction final et dans le fichier Maze.txt
        
            P[s[t][1]][s[t][0]]+=1 #Cette matrice peut servir si on veut connaitre le nombre de pas fait 
            actionsPossibles = list()
            
            for ap in actions:
                if(execution(s[t] , ap)[0] != -100):
                    actionsPossibles.append(ap)

            
            d = decision(Q , actionsPossibles , s[t] , 1 )
            action = choices(actionsPossibles , d , k=1)[0]

            #action = decision(Q , actionsPossibles , s[t] , 1 )

            a.append( execution(s[t] , action ) )

            r.append(a[t][0]) #le retour rt
            s.append(a[t][1]) #L'état st+1

            la.append(action)            
            alpha= 1/(1+N[s[t][1]][s[t][0]][action] )

            l = list()
            for ac in actions:
                l.append(Q[s[t+1][1]][s[t+1][0]][ac])     
            v = max(l)
            

            Q[s[t][1]][s[t][0]][action] = Q[s[t][1]][s[t][0]][action] + alpha * (r[t] + gamma*v - Q[s[t][1]][s[t][0]][action])            

            ct+=1

            t+=1 
       
        acc.append(ac)
        laa.append(la)
        cpt +=1
        
        y.append(len(la))
        x.append(cpt)
    return x,y,Q,P



import seaborn as sns; sns.set_theme()

#Ici on va plot le graphique
data = list()        
for i in range(15):
    PQ = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
      [[0, 0, 0, 0], [7.9766443076872555, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0.0, 0, 0], [0.0, 0.0, 0, 0.0], [0.0, 0.0, 0, 0.0], [0.0, 0, 0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0], [0.0, 0.0, 0, 0], [0, 0.0, 0, 0.0], [0.0, 0.0, 0, 0.0], [0, 0, 0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0]],
      [[0, 0, 0, 0], [8.862938119652506, 0.0, -1.0, 0], [0, 0.0, 0, 7.9766443076872555], [0, 0, 0, 0.0], [0, 0, 0, 0], [0.0, 0.0, 0.0, 0], [0, 0.0, 0.0, 0.0], [0, 0.0, 0.0, 0.0], [0.0, 0.0, 0, 0.0], [0.0, 0.0, 0, 0.0], [0, 0, 0.0, 0.0], [0, 0, 0, 0], [0.0, 0, 0.0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
      [[0, 0, 0, 0], [9.847709021836119, 0, 0.0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0.0, 0.0, 0, 0], [0.0, 0, 0.0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0], [0.0, 0.0, 0.0, 0], [0.0, 0, 0.0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0.0, 0.0, 0], [0.0, 0, 0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0]],
      [[0, 0, 0, 0], [10.941898913151244, 0.0, 0.0, 0], [0, 0, 0, 0.0], [0, 0, 0, 0], [0.0, 0.0, 0.0, 0], [0.0, 0.0, 0.0, 0.0], [0, 0.0, 0, 0.0], [0.0, 0.0, 0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0, 0.0, 0, 0.0], [0, 0, 0, 0.0], [0, 0, 0, 0], [0, 0.0, 0.0, 0], [0.0, 0, 0, 0.0], [0, 0, 0, 0]],
      [[0, 0, 0, 0], [12.157665459056936, 0, 0.0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0.0, 0.0, 0], [0.0, 0, 0.0, 0.0], [0, 0, 0, 0], [0.0, 0.0, 0.0, 0], [0.0, 0.0, 0.0, 0.0], [0, 0, 0.0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0], [0.0, 0, 0, 0], [0, 0, 0, 0], [0.0, 0, 0.0, 0], [0, 0, 0, 0]],
      [[0, 0, 0, 0], [13.50851717672993, 0, 0.0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0.0, 0.0, 0], [0.0, 0.0, 0, 0.0], [0.0, 0.0, 0.0, 0.0], [0, 0, 0.0, 0.0], [0, 0, 0, 0], [0.0, 0, 0, 0], [0, 0, 0, 0], [0.0, 0, 0.0, 0], [0, 0, 0, 0], [0.0, 0, 0.0, 0], [0, 0, 0, 0]], 
      [[0, 0, 0, 0], [15.009463529699921, 0, 0.0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0.0, 0.0, 0.0, 0], [0.0, 0, 0.0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0.0, 0.0, 0], [0.0, 0.0, 0, 0.0], [0.0, 0.0, 0.0, 0.0], [0, 0.0, 0, 0.0], [0.0, 0, 0.0, 0.0], [0, 0, 0, 0]],
      [[0, 0, 0, 0], [0.0, 16.67718169966658, 0.0, 0], [18.53020188851842, 0, 0, 0.0], [0, 0, 0, 0], [0.0, 0.0, 0, 0], [0.0, 0.0, 0, 0.0], [0.0, 0.0, 0.0, 0.0], [0, 0.0, 0.0, 0.0], [0, 0, 0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0], [0.0, 0.0, 0.0, 0], [0.0, 0, 0.0, 0.0], [0, 0, 0, 0], [0.0, 0, 0.0, 0], [0, 0, 0, 0]],
      [[0, 0, 0, 0], [0.0, 0.0, 0.0, 0], [20.58911320946491, 0, 0.0, 0.0], [0, 0, 0, 0], [0.0, 0.0, 0.0, 0], [0, 0.0, 0.0, 0.0], [0, 0, 0.0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0.0, 0, 0], [0.0, 0.0, 0.0, 0.0], [0.0, 0, 0.0, 0.0], [0, 0, 0, 0], [0, 0, 0.0, 0], [0, 0, 0, 0]], 
      [[0, 0, 0, 0], [0, 0.0, 0.0, 0], [0.0, 22.87679245496101, 0.0, 0.0], [25.41865828329001, 0.0, 0, 0.0], [0.0, 0, 0.0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0], [0.0, 0.0, 0, 0], [0.0, 0.0, 0, 0.0], [0, 0, 0, 0.0], [0, 0, 0, 0], [0, 0.0, 0.0, 0], [0.0, 0.0, 0.0, 0.0], [0.0, 0, 0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0]], 
      [[0, 0, 0, 0], [0, 0, 0, 0], [0.0, 25.41865828329001, 0.0, 0], [0, 28.242953648100013, 0.0, 0.0], [31.381059609000012, 0.0, 0.0, 0.0], [0.0, 0.0, 0, 0.0], [0.0, 0.0, 0, 0.0], [0, 0.0, 0.0, 0.0], [0, 0, 0.0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0.0, 0.0, 0], [0.0, 0, 0.0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0]], 
      [[0, 0, 0, 0], [0.0, 0.0, 0, 0], [0.0, 0, 0.0, 0.0], [0, 0, 0, 0], [0.0, 34.86784401000001, 0.0, 0], [38.742048900000015, 0.0, 0.0, 0.0], [0, 0, 0.0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0], [0.0, 90.0, 0, 0], [0, 0, 100.0, 0], [0, 0, 0, 90.0], [0, 0, 0, 0], [0.0, 0.0, 0.0, 0], [0, 0, 0, 0.0], [0, 0, 0, 0]], 
      [[0, 0, 0, 0], [0.0, 0.0, 0.0, 0], [0.0, 0.0, 0.0, 0.0], [0, 0.0, 0, 0.0], [0, 0.0, 0.0, 0.0], [43.04672100000001, 0, 0.0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0.0, 0, 81.0, 0], [0, 0, 0, 0], [0, 0, 0.0, 0], [0, 0, 0, 0], [0.0, 0, 0.0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], 
      [[0, 0, 0, 0], [0, 0.0, 0.0, 0], [0, 0, 0.0, 0.0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 47.829690000000014, 0.0, 0], [0, 53.144100000000016, 0, 0.0], [0, 59.049000000000014, 0, 0.0], [0, 65.61000000000001, 0, 0.0], [0, 0, 72.9, 0.0], [0, 0, 0, 0], [0, 0.0, 0.0, 0], [0, 0.0, 0, 0.0], [0, 0.0, 0.0, 0.0], [0, 0, 0, 0.0], [0, 0, 0, 0]],
      [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]


    v = Q_Learning( PQ , etats_labyrinthe() , actions_labyrinthe() , 0.9 , exectution_labyrinthe , init_labyrinthe , boltzmann  , est_final_labyrinthe , maze)   
    data.append(v)
"""
#On peut utiliser ce morceau de code et le mettre à la place de PQ si on veut une fonction qualité Q initialée à 0 
    Q = list()
    for i in range(16):
        jl= list()
        for j in range(16):
            kl= list()
            for k in range(4):
                kl.append(0)
            jl.append(kl)
        Q.append(jl)    
"""


        
        

#######################################--AFFICHAGE--######################################





#Cette partie là sert à faire une HeatMap à partir de la fonction qualité passée en paramètre


data = list()
data.append(Q_Learning( PQ , etats_labyrinthe() , actions_labyrinthe() , 0.9 , exectution_labyrinthe , init_labyrinthe , boltzmann  , est_final_labyrinthe , maze)   )


QModifier = data[0][2]

il = list()
for i in range(16):
    jl = list()
    for j in range(16):
        jl.append(max(QModifier[j][i]))
    il.append(jl)



    
uniform_data = il
ax = sns.heatmap(uniform_data)


"""
for path in data:
    plt.plot(path[0], path[1], color='darkgrey', linewidth = 0.6, markerfacecolor='black', markersize=5)

plt.xlabel('x - Episode')

plt.ylabel('y - Number of steps to leave')
  
plt.title('Learning curve')


plt.show()
"""