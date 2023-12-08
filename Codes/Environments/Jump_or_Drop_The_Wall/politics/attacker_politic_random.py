import random

from Codes.Environments.Jump_or_Drop_The_Wall.politics.attacker_politic import attacker_politic

class attacker_politic_random(attacker_politic):
    def __init__(self):
        pass

    def get_action(self, env, attacker):
        action_space = attacker.actions
        return random.choice(action_space)