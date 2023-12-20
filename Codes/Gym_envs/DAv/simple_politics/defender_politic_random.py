import random

from Codes.Gym_envs.DAv.simple_politics.defender_politic import defender_politic


class defender_politic_random(defender_politic):
    def __init__(self):
        pass

    def get_action(self, env, defender):
        action_space = defender.get_actions()
        return random.choice(action_space)
