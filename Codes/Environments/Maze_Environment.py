#####################################Fonctions utiles#####################################
def conversion(c):
    """
    This function will convert the characters of the maze into numbers :
        * -> -100
        ' ' -> 0
        O -> -1
        V -> 100
    Parameters :
        c : character
    Returns :
        int : number
    """
    if c == "*":
        return -100
    elif c == " ":
        return 0
    elif c == "O":
        return -1
    elif c == "V":
        return 100


def board():
    """return the board of the maze

    Returns:
        list: board of the maze
    """
    file = open("../Environments/Maze.txt", "r")

    maze = list()
    for line in file:
        l = list()
        for character in line:
            if character != "\n":
                l.append(conversion(character))
        maze.append(l)

    maze.reverse()
    return maze


def etats_labyrinthe():
    """
    We define all the possible states of the maze.
    """
    l = list()
    for i in range(16):
        for j in range(16):
            l.append([i, j])
    return l


def actions_labyrinthe():
    """
    This function will allow us to have the list of possible actions for the maze game.
    We will assume that:
        0 -> go right
        1 -> go up
        2 -> go right
        3 -> go down
    Returns
    -------
    list
        actions.
    """
    return [0, 1, 2, 3]


def exectution_labyrinthe(etat, action):
    """
    This function will execute the action passed as a parameter in the environment of the maze and return:
        (return, state) which are the things to observe once the action is performed
    """
    p = etat.copy()
    if action == 0:
        if p[1] + 1 > len(maze[0]) - 1:
            return (maze[p[0]][p[1]], p)
        p[1] += 1
        return (maze[p[0]][p[1]], p)
    if action == 1:
        if p[0] + 1 > len(maze) - 1:
            return (maze[p[0]][p[1]], p)
        p[0] += 1
        return (maze[p[0]][p[1]], p)
    if action == 2:
        if p[1] - 1 < 0:
            return (maze[p[0]][p[1]], p)
        p[1] -= 1
        return (maze[p[0]][p[1]], p)
    if action == 3:
        if p[0] - 1 < 0:
            return (maze[p[0]][p[1]], p)
        p[0] -= 1
        return (maze[p[0]][p[1]], p)


def init_labyrinthe():
    """
    Initial state of the maze
    """
    return [1, 1]


def if_final_state(s):
    """
    return True if the state s is the final state
    """
    return s == [10, 11]


################################# Non-stationnary ####################################################
def deplacement1(maze, final, episode):
    """
    This function returns the maze passed as a parameter but in moving the final state.
    Every 2 episodes it will move 1 to the left, otherwise to the right
    """
    if episode % 2 == 0:
        coo = exectution_labyrinthe(final, 2)[1]
        maze[coo[0]][coo[1]], maze[final[0]][final[1]] = (
            maze[final[0]][final[1]],
            maze[coo[0]][coo[1]],
        )
        return coo
    else:
        coo = exectution_labyrinthe(final, 0)[1]
        maze[coo[0]][coo[1]], maze[final[0]][final[1]] = (
            maze[final[0]][final[1]],
            maze[coo[0]][coo[1]],
        )
        return coo


def deplacement2(maze, final, episode):
    """
    This function changes the final state of the maze by moving it.
    One episode on 2 it will move from the case (6,3) to the (3,6)
    """
    if episode % 2 == 0:
        coo = [3, 6]
        maze[coo[0]][coo[1]], maze[final[0]][final[1]] = (
            maze[final[0]][final[1]],
            maze[coo[0]][coo[1]],
        )
        return coo
    else:
        coo = [6, 3]
        maze[coo[0]][coo[1]], maze[final[0]][final[1]] = (
            maze[final[0]][final[1]],
            maze[coo[0]][coo[1]],
        )
        return coo


def teleportation(maze, final, episode):
    """
    Like the previous function but it will move the final state to either (10,4) or (7,3)
    """
    if episode % 2 == 0:
        coo = [10, 4]
        maze[coo[0]][coo[1]], maze[final[0]][final[1]] = (
            maze[final[0]][final[1]],
            maze[coo[0]][coo[1]],
        )
        return coo
    else:
        coo = [7, 3]
        maze[coo[0]][coo[1]], maze[final[0]][final[1]] = (
            maze[final[0]][final[1]],
            maze[coo[0]][coo[1]],
        )

        return coo
