import random

from Codes.Gym_envs.DAv.simple_politics.attacker_politic import attacker_politic


class attacker_politic_random(attacker_politic):
    def get_action(self, env, attacker):
        action_space = attacker.get_actions()
        return random.choice(action_space)
