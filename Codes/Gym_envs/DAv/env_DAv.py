from typing import Dict, Tuple

import gymnasium as gym
import numpy as np

from Codes.Gym_envs.DAv.map import Map_DAv
from Codes.Gym_envs.DAv.players.defender import Defender
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
        number_of_defenders: int = 2,
        map_size: tuple = (20, 20),
        step_limit: int = 500,
        rendering: bool = False,
        *args,
        **kwargs,
    ) -> None:
        self.action_space = gym.spaces.Discrete(4)
        self.map_size = map_size
        self.number_of_attackers = number_of_attackers
        self.number_of_defenders = number_of_defenders
        min_x, max_x = 0, map_size[0]
        min_y, max_y = 0, map_size[1]
        self.observation_space = gym.spaces.Dict(
            {
                "attackers_position": gym.spaces.Box(
                    low=np.array([min_x, min_y] * number_of_attackers),
                    high=np.array([max_x, max_y] * number_of_attackers),
                    dtype=np.float32,
                ),
                "defenders_position": gym.spaces.Box(
                    low=np.array([min_x, min_y] * number_of_defenders),
                    high=np.array([max_x, max_y] * number_of_defenders),
                    dtype=np.float32,
                ),
                "walls_position": gym.spaces.Box(
                    low=np.array([min_x, min_y] * map_size[0] * map_size[1]),
                    high=np.array([max_x, max_y] * map_size[0] * map_size[1]),
                    dtype=np.float32,
                ),
            }
        )
        self.step_limit = step_limit
        if rendering:
            self.rendering = Render_DAv()
        self.map = None
        self.players = None
        self.attackers = None
        self.defenders = None
        self.walls = None
        self.steps = None
        self.terminated = None
        self.truncated = None
        self.reset()

    def _get_obs(self) -> Dict:
        """
        The observation of the environment is a dict composed of a numpy arrays of:
            - The position of the attackers
            - The position of the defenders
            - The position of the walls
        """
        return {
            "attackers_position": np.array(
                [attacker.get_position() for attacker in self.attackers]
            ),
            "defenders_position": np.array(
                [
                    defender.get_position()
                    for defender in self.defenders
                    if defender.is_alive()
                ]
            ),
            "walls_position": np.array(
                [wall.get_position() for wall in self.walls if (not wall.is_broken())]
            ),
        }

    def reset(self, seed=None) -> None:
        self.map = Map_DAv(
            map_size=self.map_size,
            number_of_attackers=self.number_of_attackers,
            number_of_defenders=self.number_of_defenders,
            step_limit=self.step_limit,
        )
        self.players = self.map.get_attackers() + self.map.get_defenders()
        self.attackers = self.map.get_attackers()
        self.defenders = self.map.get_defenders()
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

        # Compute the rewards of the defenders
        defenders_reward = []
        for i, defender in enumerate(
            [deff for deff in self.defenders if deff.is_alive()]
        ):
            reward = defender.step(action[self.number_of_attackers + i])
            defenders_reward.append(reward)
        rewards.append(defenders_reward)

        self.steps += 1

        # We are done only when there is no defenders alive an more.
        self.terminated = all(
            [not defender.is_alive() for defender in self.map.get_defenders()]
        )
        self.truncated = self.steps > self.step_limit
        return self._get_obs(), rewards, self.terminated, self.truncated, info

    def render(self):
        """
        Render the environment using matplotlib.
        """
        self.rendering.render_env(self.map, self.steps)

    def kill_the_defender(self, defender_position):
        """
        Kills the defender when touched by an attacker.
        """
        if isinstance(self.map.get_cell(defender_position), Defender):
            self.map.get_cell(defender_position).kill()
            self.map.assign_element(defender_position, 0.0)

    def get_defenders(self):
        """
        Returns the defenders of the environment.
        """
        return self.map.get_defenders()

    def get_attackers(self):
        """
        Returns the attackers of the environment.
        """
        return self.map.get_attackers()

    def get_map(self):
        return self.map

    def close(self):
        pass
