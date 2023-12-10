import random

from Codes.Gym_envs.DAv.simple_politics.defenser_politic import defenser_politic


class defenser_politic_random(defenser_politic):
    def __init__(self):
        pass

    def get_action(self, env, defenser):
        action_space = defenser.get_actions()
        return random.choice(action_space)
