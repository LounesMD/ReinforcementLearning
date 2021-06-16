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


"""
Pour l'algorithme de Q-learning qui va suivre, on va partir du fait que chaque action nous permet d'avoir un retour.
Par exemple, pour l'exemple du labyrinthe, on va gagner 0 point à chaque fois qu'on va arriver sur une cellule qui va 
nous rapprocher de la fin, et  -100 points si on va sur un mur (ce sera un critère pour vérifier si une action est possibles ou non).

Pour savoir si notre épisode est finie, on va partir du principe qu'il faut utiliser une fonction qui détermine si l'état dans le quel on se trouve est final ou non.
"""


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
        coo = [10,11]
        maze[coo[0]][coo[1]] , maze[final[0]][final[1]] =   maze[final[0]][final[1]] ,  maze[coo[0]][coo[1]]
        return coo
    else:
        coo = [7,3]
        maze[coo[0]][coo[1]] , maze[final[0]][final[1]] =   maze[final[0]][final[1]] ,  maze[coo[0]][coo[1]]

        return coo

CSI="\x1B["
def affichage2_0(maze , s , final):    
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
        

def Q_Learning(etats , actions , gamma , execution , init , decision , final , environnement):
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
    
    Q = list()
    for i in range(ligne):
        jl= list()
        for j in range(colonne):
            kl= list()
            for k in range(len(actions)):
                kl.append(0)
            jl.append(kl)
        Q.append(jl)  


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
    
    laa = list()
    acc = list()
    cpt = 0
    x = list()
    y = list()
    final = [10,11]
    while(cpt < 70): #On va faire 70 épisodes
    
        s = list()
        s.append(init())
        ac = list()
        t=0
        r = list()
        a = list()
        la = list()
        ct = 0
        final = teleportation(maze , final , cpt)
        
        val =  time.perf_counter()
        
        while  s[t] != final: #r[t]!=100     
            print(s[t] , final)
            print("Episode : "+str(cpt))
            print("Action : "+str(ct))
                
            val = time.perf_counter()
            
            
            actionsPossibles = list()
            for ap in actions:
                if(execution(s[t] , ap)[0] != -100):
                    actionsPossibles.append(ap)

            
            d = decision(Q , actionsPossibles , s[t] , 60 )
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
            
            affichage2_0(maze , s[t] , final)
            print("-----------------------------------")
        acc.append(ac)
        laa.append(la)
        cpt +=1
        
        y.append(len(la))
        x.append(cpt)
    print(len(laa[69]))
    return x,y



#Ici on va plot le graphique
data = list()        
for i in range(1):
    data.append(Q_Learning(etats_labyrinthe() , actions_labyrinthe() , 0.9 , exectution_labyrinthe , init_labyrinthe , boltzmann  , est_final_labyrinthe , maze)    )


for path in data:
    plt.plot(path[0], path[1], color='darkgrey', linewidth = 0.6, markerfacecolor='black', markersize=5)

plt.xlabel('x - Episode')

plt.ylabel('y - Number of steps to leave')
  
plt.title('Learning curve')

plt.savefig('OnPolicyTeleportation.png')

plt.show()

