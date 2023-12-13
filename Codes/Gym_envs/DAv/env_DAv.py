from typing import Tuple

import gymnasium as gym
import numpy as np
import torch

from Codes.Gym_envs.DAv.map import Map_DAv
from Codes.Gym_envs.DAv.players.defenser import Defenser
from Codes.Gym_envs.DAv.render import Render_DAv
from Codes.Gym_envs.DAv.utils.observation import BinaryMapObservation


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
    - A binary_map, used to get a tensor representation of the map. The tensor is composed of three slices:
        1. A first binary tensor of the attackers/defenders positions
        2. A second binary tensor of the defenders/attackers positions
        3. A third binary tensor of the walls.

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
        map_size: tuple = (15, 15),
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
        self.map = self.reset()
        self.players = self.map.get_attackers() + self.map.get_defensers()
        self.attackers = self.map.get_attackers()
        self.defensers = self.map.get_defensers()
        self.walls = self.map.get_walls()
        self.rendering = Render_DAv()
        self.binary_map = self._init_binary_map()
        self.steps = 0
        self.terminated = False

    def _init_binary_map(self) -> list:
        walls_tensor = np.zeros(
            shape=(self.map_size[0], self.map_size[1])
        )  # At the initialisation, there is no wall.

        # Initialisation of the attackers position
        attackers_tensor = np.zeros(shape=(self.map_size[0], self.map_size[1]))
        for attacker in self.attackers:
            attackers_tensor[attacker.get_position()[0]][
                attacker.get_position()[1]
            ] = 1.0

        # Initialisation of the defensers position
        defensers_tensor = np.zeros(shape=(self.map_size[0], self.map_size[1]))
        for defenser in self.defensers:
            defensers_tensor[defenser.get_position()[0]][
                defenser.get_position()[1]
            ] = 1.0

        return BinaryMapObservation(
            attackers_tensor, defensers_tensor, walls_tensor, self.map_size
        )

    def _get_obs(self) -> BinaryMapObservation:
        return self.binary_map

    def reset(self) -> Map_DAv:
        map = Map_DAv(
            map_size=self.map_size,
            number_of_attackers=self.number_of_attackers,
            number_of_defensers=self.number_of_defensers,
        )
        return map

    def step(self, action) -> Tuple[np.array, list, bool, dict]:
        """
        One step for each player of the environment.

        args:
            action(list): A list of one step action of each player.

        TODO: Find a more performant way to udpate the positions.
        """
        info = (
            dict()
        )  # For the moment there is not info. Maybe some action masking later.

        rewards = list()
        # Compute the rewards of the attackers
        attackers_reward = 0
        for i, attacker in enumerate(self.attackers):
            self.binary_map.update_attackers_tensor(attacker.get_position(), 0.0)
            reward = attacker.step(action[i])
            attackers_reward += reward
            self.binary_map.update_attackers_tensor(attacker.get_position(), 1.0)

        rewards.append(attackers_reward)

        # Compute the rewards of the defensers
        defensers_reward = 0
        for i, defenser in enumerate(self.defensers):
            if defenser.is_alive():
                self.binary_map.update_defensers_tensor(defenser.get_position(), 0.0)
                reward = defenser.step(
                    action[self.number_of_attackers - 1 + i]
                )  # -1 Because the index starts at 0.
                defensers_reward += reward
                self.binary_map.update_defensers_tensor(defenser.get_position(), 1.0)
        rewards.append(defensers_reward)
        # Update the position of the walls.
        self.udpate_walls_postion()

        # We are done only when there is no defensers alive an more.
        self.terminated = all(
            [not defenser.is_alive() for defenser in self.map.get_defensers()]
        )
        self.steps += 1
        truncated = self.terminated  # For now there is no truncated episode
        return self._get_obs(), rewards, self.terminated, truncated, info

    def udpate_walls_postion(self):
        """
        Update the binary position of the walls.
        """
        for wall in self.walls:
            if wall.is_broken():
                self.binary_map.update_walls_tensor(wall.get_position(), 0.0)
            else:
                self.binary_map.update_walls_tensor(wall.get_position(), 1.0)

    def render(self):
        """
        Render the environment using matplotlib.
        """
        self.rendering.render_env(self.map)

    def kill_the_defenser(self, defenser_position):
        """
        Kills the defenser when touched by an attacker.
        """
        if isinstance(self.map.get_cell(defenser_position), Defenser):
            self.map.get_cell(defenser_position).kill()
            self.map.assign_element(defenser_position, 0.0)
            self.binary_map.update_defensers_tensor(defenser_position, 0.0)

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
