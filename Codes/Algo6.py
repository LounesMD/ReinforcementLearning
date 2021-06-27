# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 11:56:12 2021

@author: Lounès
"""
from random import choice
from random import choices

import matplotlib.pyplot as plt
import seaborn as sns; sns.set_theme()
import math


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
        
        
        
def Eps_Gloutonne( Q , act ,  etat , epsilon ):
    """
    Fonction epsilon-gloutonne 

    Parameters
    ----------
    Q : list
        fonction qualité courante.
    act : list
        listes des actions possibles.
    epsilon : int
        entier epsilon.
    etat : list
        coordonée de l'état courant.

    Returns
    -------
    int
        renvoie l'action à faire en ayant fait un choix epsilon-glouton.
    """
    v = choices( [1,2] , weights = [1-epsilon , epsilon] , k=1 ) #Cela va nous permettre d'avoir soit un choix glouton, soit aléatoire

    if v ==[1]:        
        li = list()
        for action in act:
            li.append((Q[etat[1]][etat[0]][action] , action))

        max_val= max(li , key = lambda x: x[0])
        return max_val[1]

    else: 
        return choice(act)
##########################################################################################





"""
Proposition d'algrithme Q(lambda)
"""
def Q_Lambda(etats , actions , gamma , lambd , environnement , init , execution , decision , alpha , final ):

        
    ligne = len(environnement)
    colonne =  len(environnement[0])
    
    Q = list()
    for i in range(ligne):
        jl= list()
        for j in range(colonne):
            kl= list()
            for k in range(len(actions())):
                kl.append(0)
            jl.append(kl)
        Q.append(jl)  
    cpt = 0
    x = list()
    y = list()
    laa = list()

    while cpt < 70:   
        la= list()
        #Cette fonction e(s,a) va nous permettre de connaitre l'éligibilité d'une paure etat-action
        E = list()
        for i in range(ligne):
            jl= list()
            for j in range(colonne):
                kl= list()
                for k in range(len(actions())):
                    kl.append(0)
                jl.append(kl)
            E.append(jl)   
                    
        t = 0
        r = list()#Liste des retours possibles
        d = list()
        s = list()
        a = list() #Dans a on stock les actions successives
        observation = list()#Dans observation on stock les couples retour-etatt+1
        #Etat initial
        s.append(init())
                    
        actionsP = list()
        for ap in actions():
            if(execution(s[t] , ap)[0] != -100):
                actionsP.append(ap)
            
        d = decision(Q , actionsP , s[t] , 0.5 )    
        a.append(choices(actionsP , d , k=1)[0])
        observation.append(execution(s[t] , a[t] ))
        while  not final(s[t]) :
            #Là on va émettre l'action at et observer rt-st+1            
            r.append(observation[t][0]) #le retour rt         
            s.append(observation[t][1]) #L'état st+1                        
            #affichage2_0(maze , s[t] , [10,11])
            la.append(a[t]) 
            #On va choisir l'action at+1 à émettre dans st+1
            actionsPossibles = list()
            #print(s[t] , s[t+1])
            for ap in actions():
                if(execution(s[t+1] , ap)[0] != -100):
                    actionsPossibles.append(ap)          
            
            #Cas Boltzmann
            d = decision(Q , actionsPossibles , s[t+1] , 0.5 )    
            a.append(choices(actionsPossibles , d , k=1)[0])
            observation.append( execution(s[t+1] , a[t+1] ) )    
            
            
            #################################################################################
            #On va chercher le a*
            l = list()
            #print(actionsPossibles)            
            for action in actionsPossibles:
                l.append( ( Q[s[t+1][1]][s[t+1][0]][action] , action ) )
            a_opti = max( l , key = lambda x:x[0])[1]
            #################################################################################                                                
            delta = r[t] + gamma * Q[s[t+1][1]][s[t+1][0]][a_opti] - Q[s[t][1]][s[t][0]][a[t]]            
            
            E[s[t][1]][s[t][0]][a[t]] += 1
            
            for etat in etats() :
                for action in actions():
                    Q[etat[1]][etat[0]][action] = Q[etat[1]][etat[0]][action] + alpha * delta *  E[etat[1]][etat[0]][action]
                    E[etat[1]][etat[0]][action] = gamma * lambd * E[etat[1]][etat[0]][action]
            t+=1
        
        cpt += 1
        laa.append(la)
        x.append(cpt)
        y.append(len(la))
    print(len(laa[-1])) #Cela va nous permettre de connaitre le nombre de pas fait pour le dernier épisode
    return x,y,Q


################################################---AFFICHAGE---#############################################################
"""
#Affichage de la Learning Curve
data = list()        
for i in range(15):
    v = Q_Lambda(etats_labyrinthe , actions_labyrinthe , 0.9 , 0.8 , maze , init_labyrinthe ,exectution_labyrinthe,  boltzmann , 0.85 , est_final_labyrinthe)
    data.append(v )

for path in data:
    plt.plot(path[0], path[1], color='darkgrey', linewidth = 0.4, markerfacecolor='black', markersize=5)

plt.xlabel('x - Episode')

plt.ylabel('y - Number of steps to leave')
  
plt.title('Learning curve')


plt.show()


#Affichage de la HeatMap
"""
QModifier = Q_Lambda(etats_labyrinthe , actions_labyrinthe , 0.9 , 0.8 , maze , init_labyrinthe ,exectution_labyrinthe,  boltzmann , 0.85 , est_final_labyrinthe)

il = list()
for i in range(16):
    jl = list()
    for j in range(16):
        jl.append(max(QModifier[j][i]))
    il.append(jl)
uniform_data = il
ax = sns.heatmap(uniform_data)


###########################################################################################################################
