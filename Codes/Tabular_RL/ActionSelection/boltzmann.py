import math


def boltzmann(Q, actions, state, to):
    """
    Action selection using the Boltzmann uquation.
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
    l = list()
    for action in actions:
        p = 0
        ex = math.exp((Q[state[0]][state[1]][state[2]][state[3]][action]) / to)  #
        # ex = math.exp((Q[state[0]][state[1]][action])/to) #

        v = 0
        for a in actions:
            v += math.exp((Q[state[0]][state[1]][state[2]][state[3]][a]) / to)
            # v+= math.exp((Q[state[0]][state[1]][a])/to)
        p = ex / v
        l.append(p)
    return l
