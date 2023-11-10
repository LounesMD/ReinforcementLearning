# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 11:56:12 2022

@author: Lounès Meddahi

Quality Function based algorithm :

Monte Carlo Algorithm soon available.
I still have to fix a bug
"""

from random import choices

from Utile import *


def MonteCarlo(states , actions , gamma , execution , PossibleActions , decision , final , nbEpochs , AccessibleState,environnement):
    """ Monte Carlo algorithms

    Args:
        states (list): _description_
        actions (list): _description_
        gamma (_type_): _description_
        environnement (_type_): _description_
        init (_type_): _description_
        execution (_type_): _description_
        final (_type_): _description_
        nbEpochs (_type_): _description_
        PossibleActions (function) : this function takes as arguments (environnement,state) and returns all possible actions from the state.
        Mainly usefull to don't compute the possible actions from the state directly in the algorithm.
    """
    Q = dict()
    for state in states:
        st = str(state)
        Q[st] = dict()
        for action in actions:
            ac = str(action)
            Q[st][ac] = 0
    
    n = nbEpochs

    for state in states :
        print(state)
        if(AccessibleState(environnement , state)):
            for action in actions :
                R = 0 # R for reward 
                for i in range(n):
                    e = state
                    b = action
                    j = 0
                    sum = 0

                    while not final(e) :
                        observation = list() #In observation we stock the tupple (reward,state) after executing the action b in e
                        actionsPossibles = PossibleActions(actions , e , execution)

                        # TODO : Think about greedy policy instead of using the Boltzmann function

                        # If we use a non deterministic choice function (such as Boltzmann)
                        d = decision(Q , actionsPossibles , e , 1 ) #
                        action = choices(actionsPossibles , d , k=1)[0]  # We stock in `action` the action to do

                        # If we use a deterministic choice function (such as greedy)
                        #action = decision(Q , actionsPossibles , s[t] , 1 )
                        reward,e = execution(e , action) #We execute the action in the state e and observe the new state 'e_state' and the reward
                        sum += (gamma**j)*reward

                        j += 1
                    R += R + sum
                Q[str(state)][str(action)] = R/n
    return Q
                

def PossibleActionsMaze(actions , state , execution):
    """ In our mazes, if the reward is -100 it means that we can go into this cell"""
    actionsP = list()
    for ap in actions :
        if(execution(state , ap)[0] != -100):
            actionsP.append(ap)
    return actionsP

def accessible(environnement , state ):
    return (environnement[state[0]][state[1]] != -100)

Q = MonteCarlo(etats_labyrinthe() , actions_labyrinthe() , 0.5 , exectution_labyrinthe , PossibleActionsMaze , boltzmannP , est_final_labyrinthe , 100 , accessible , maze)               
print(Q)
