import random

from Codes.Environments.Jump_or_Drop_The_Wall.politics.defenser_politic import defenser_politic

class defenser_politic_random(defenser_politic):
    def __init__(self):
        pass

    def get_action(self, env, defenser):
        action_space = defenser.actions
        return random.choice(action_space)