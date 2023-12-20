from typing import Dict, Tuple

import gymnasium as gym
import numpy as np

from Codes.Gym_envs.DAv.map import Map_DAv
from Codes.Gym_envs.DAv.players.defenser import Defenser
from Codes.Gym_envs.DAv.render import Render_DAv


class Env_DAv(gym.Env):
    """
    DAv Environment. This is how this environment works:
    - The goal of DAv is to provide a simple environment where attackers and defenders face each other.
    - The goal of the Attackers is to touch a Defender. To do so, they have to be in a neighboring cell of
    a defender and perform the action that moves them to the defender's cell.
    - On their side, the defenders must run away from the attackers. To help them in this task, they
    can drop walls to block the path of the attackers. Of course, the attackers can destroy the walls.

    The implementation of this environment, called by using 'env = gym.make("env_DAv-v0")', is as follows:
    - A map, implemented using lists, that stores the Defenders, Attackers, and Walls in their correct positions and has zeros everywhere else.

        Two representations of this map can be accessible:
            1. From the attackers' point of view, their tensor is put first.
            2. From the defenders' point of view, their tensor is put first.
    - Rewards:
        - A +1 reward is given to a defender at each step the defender is alive.
        - A -1 reward is given for the rest of the game if the defender is dead.
        - A +0 reward is given to a defender at each step.
        - A +1 reward is given to an attacker each time it touches a defender.
    """

    def __init__(
        self,
        number_of_attackers: int = 2,
        number_of_defensers: int = 2,
        map_size: tuple = (20, 20),
        step_limit: int = 500,
        rendering: bool = False,
        *args,
        **kwargs,
    ) -> None:
        self.action_space = gym.spaces.Discrete(4)
        self.map_size = map_size
        self.observation_space = gym.spaces.Box(
            shape=(3, self.map_size[0], self.map_size[1]), low=0, high=1
        )
        self.number_of_attackers = number_of_attackers
        self.number_of_defensers = number_of_defensers
        self.step_limit = step_limit
        if rendering:
            self.rendering = Render_DAv()
        self.map = None
        self.players = None
        self.attackers = None
        self.defensers = None
        self.walls = None
        self.steps = None
        self.terminated = None
        self.truncated = None
        self.reset()

    def _get_obs(self) -> Dict:
        """
        The observation of the environment is a dict composed of a numpy arrays of:
            - The position of the attackers
            - The position of the defensers
            - The position of the walls
        """
        return {
            "attackers_position": np.array(
                [attacker.get_position() for attacker in self.attackers]
            ),
            "defensers_position": np.array(
                [
                    defenser.get_position()
                    for defenser in self.defensers
                    if defenser.is_alive()
                ]
            ),
            "walls_position": np.array(
                [wall.get_position() for wall in self.walls if (not wall.is_broken())]
            ),
        }

    def reset(self) -> None:
        self.map = Map_DAv(
            map_size=self.map_size,
            number_of_attackers=self.number_of_attackers,
            number_of_defensers=self.number_of_defensers,
            step_limit=self.step_limit,
        )
        self.players = self.map.get_attackers() + self.map.get_defensers()
        self.attackers = self.map.get_attackers()
        self.defensers = self.map.get_defensers()
        self.walls = self.map.get_walls()
        self.steps = 0
        self.terminated = False
        self.truncated = False

    def step(self, action) -> Tuple[np.array, list, bool, dict]:
        """
        One step for each player of the environment.

        args:
            action(list): A list of one step action of each player.
        """
        info = (
            dict()
        )  # For the moment there is not info. Maybe some action masking later.

        rewards = list()
        # Compute the rewards of the attackers
        attackers_reward = []
        for i, attacker in enumerate(self.attackers):
            reward = attacker.step(action[i])
            attackers_reward.append(reward)

        rewards.append(attackers_reward)

        # Compute the rewards of the defensers
        defensers_reward = []
        for i, defenser in enumerate(
            [deff for deff in self.defensers if deff.is_alive()]
        ):
            reward = defenser.step(action[self.number_of_attackers + i])
            defensers_reward.append(reward)
        rewards.append(defensers_reward)

        self.steps += 1

        # We are done only when there is no defensers alive an more.
        self.terminated = all(
            [not defenser.is_alive() for defenser in self.map.get_defensers()]
        )
        self.truncated = self.steps > self.step_limit
        return self._get_obs(), rewards, self.terminated, self.truncated, info

    def render(self):
        """
        Render the environment using matplotlib.
        """
        self.rendering.render_env(self.map, self.steps)

    def kill_the_defenser(self, defenser_position):
        """
        Kills the defenser when touched by an attacker.
        """
        if isinstance(self.map.get_cell(defenser_position), Defenser):
            self.map.get_cell(defenser_position).kill()
            self.map.assign_element(defenser_position, 0.0)

    def get_defensers(self):
        """
        Returns the defensers of the environment.
        """
        return self.map.get_defensers()

    def get_attackers(self):
        """
        Returns the attackers of the environment.
        """
        return self.map.get_attackers()

    def get_map(self):
        return self.map

    def close(self):
        pass
