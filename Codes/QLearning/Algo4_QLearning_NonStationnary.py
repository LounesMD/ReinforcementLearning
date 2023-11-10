"""
Created on Tue Jun  8 11:03:04 2021

@author: Lounès

Quality Function based algorithm :

This file gives an implementation of the Q-Learning algorithm applied to an non-stationnary environnement.


"""


import time
from random import choice
from random import choices
import math
import matplotlib.pyplot as plt
import numpy as np
import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set_theme()
        
        
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
CE FICHIER EST L'IMPLEMENTATION DE LA PARTIE 3.5.5.2 càd la partie qui étudie le comportement de la fonction de 
Q-Learning pour un environnement évolutif.
"""


#####################################Fonctions utiles#####################################
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
    Function that will choose the action to do regarding the Boltzmann model

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
    Greedy function 

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
    
def deplacement(maze , final , episode):
    actions = [0,1,2,3]
    actionsPossibles = list()
    for k in actions:
        if exectution_labyrinthe(final,k)[0] != 100 :
            actionsPossibles.append(k)
            
    action = choice(actionsPossibles)
    nv_final = exectution_labyrinthe(final,action)
    return nv_final[1]
    



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
        
        

""" #Si on a envie de passer du grand labyrinthe au petit labyrinthe
file = open("Maze1.txt","r")
maze = list()
for line in file:
    l = list()
    for character in line:
        if(character != '\n'):
            l.append(conversion(character))
    maze.append(l)

maze.reverse()
"""

    


def deplacement2(maze , final , episode):
    """
    /!\/!\/!\A utiliser sur Maze1.txt (le petit labyrinthe)
    fonction qui renvoi le labyrinthe passé en paramètre mais en déplacent l'état final en le téléportant.
    Un épisode sur 2 il va se téléporter de la case (6,3) à la (3,6)
    """    
    if episode%2 == 0:
        coo = [3,6]
        maze[coo[0]][coo[1]] , maze[final[0]][final[1]] =   maze[final[0]][final[1]] ,  maze[coo[0]][coo[1]]
        return coo
    else:
        coo = [6,3]
        maze[coo[0]][coo[1]] , maze[final[0]][final[1]] =   maze[final[0]][final[1]] ,  maze[coo[0]][coo[1]]
        return coo
    
    
def exectution_labyrinthe2(maze, etat,action):
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


    
def deplacement_petit(maze , final , episode):
    """
    Fonction qui permet à l'état final de faire des petits déplacements tous les tours
    (càd seulement une action aléatoire)

    Parameters
    ----------
    maze : TYPE
        DESCRIPTION.
    final : TYPE
        ancien état final.
    episode : TYPE
        DESCRIPTION.

    Returns
    -------
    nv_final : TYPE
        coordonnées après avoir fait son action.

    """
    actions = [0,1,2,3]
    actionsPossibles = list()
    for k in actions:
        v = exectution_labyrinthe2(maze , final,k)[0]
        if  v != -100 and v!=-1 :
            actionsPossibles.append(k)    
        
    action = choice(actionsPossibles)
    nv_final = exectution_labyrinthe2(maze,final,action)[1]
    maze[nv_final[0]][nv_final[1]] , maze[final[0]][final[1]] =   maze[final[0]][final[1]] ,  maze[nv_final[0]][nv_final[1]]
    
    return nv_final

##########################################################################################


        

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
    
    print(cpt)
    
    while(cpt < 70): #On va faire 70 épisodes
        
        s = list()
        s.append(init())
        ac = list()
        t=0
        r = list()
        a = list()
        la = list()
        ct = 0
        
        val = time.perf_counter()
        
        #final = teleportation(maze , final , cpt) #A utiliser pour que la sortie se TP 

        final = [10,11] #A utiliser pour l'état final de base
        while  s[t] != final: #r[t]!=100    
            
            final = deplacement_petit(maze , final , cpt) #A utiliser si on veut que la sortie fasse des actions aléatoires
            
            #SI ON VEUT AFFICHER LE LABYRINTHE            
            #print(s[t] , final)
            #print("Episode : "+str(cpt))
            #print("Action : "+str(ct))
            #while(time.perf_counter() - val < 0.1):
            #   pass
                
            #val = time.perf_counter()
            
            
            actionsPossibles = list()
            for ap in actions:
                if(execution(s[t] , ap)[0] != -100):
                    actionsPossibles.append(ap)
                
            d = decision(Q , actionsPossibles , s[t] , 25 )
            
            action = choices(actionsPossibles , d , k=1)[0]

            #action = decision(Q , actionsPossibles , s[t] , 1 ) #Cas glouton

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
            #FONCTIONS D AFFICHAGES
            #affichage2_0(maze , s[t] , final)            
            #print("---------------------------------------------")
            
            
        acc.append(ac)
        laa.append(la)
        cpt +=1
        
        y.append(len(la))
        x.append(cpt)        
    return x,y,Q



#######################################--AFFICHAGE_1--######################################


#Ici on va plot le graphique pour un environnement qui a un état final qui se téléporte
data = list()        
for i in range(1):
    data.append(Q_Learning(etats_labyrinthe() , actions_labyrinthe() , 0.9 , exectution_labyrinthe , init_labyrinthe , boltzmann  , est_final_labyrinthe , maze)    )

    
for path in data:
    plt.plot(path[0], path[1], color='darkgrey', linewidth = 0.6, markerfacecolor='black', markersize=5)

plt.xlabel('x - Episode')

plt.ylabel('y - Number of steps to leave')
  
plt.title('Learning curve')


plt.show()


"""
#Ici on va plot la HeatMap environnement qui a un état final qui se téléporte (entre 2 endroits)
Q = Q_Learning(etats_labyrinthe() , actions_labyrinthe() , 0.9 , exectution_labyrinthe , init_labyrinthe , boltzmann  , est_final_labyrinthe , maze)[2]
il = list()
for i in range(16):
    jl = list()
    for j in range(16):
        jl.append(max(Q[j][i]))
    il.append(jl)
    
uniform_data = il
ax = sns.heatmap(uniform_data)

"""
###########################################################################################
