import gymnasium as gym

from Codes.Gym_envs.DAv.map import Map_DAv
from Codes.Gym_envs.DAv.players.defenser import Defenser
from Codes.Gym_envs.DAv.render import Render_DAv


class Env_DAv(gym.Env):
    def __init__(
        self,
        number_of_attackers: int = 2,
        number_of_defensers: int = 2,
        map_size: tuple = (15, 15),
        *args,
        **kwargs,
    ) -> None:
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Discrete(map_size[0] * map_size[1])

        self.number_of_attackers = number_of_attackers
        self.number_of_defensers = number_of_defensers
        self.map_size = map_size
        self.map = self.reset()
        self.players = self.map.get_attackers() + self.map.get_defensers()
        self.rendering = Render_DAv()
        self.steps = 0
        self.terminated = False

    def _get_obs(self):
        return self.map

    def reset(self):
        map = Map_DAv(
            map_size=self.map_size,
            number_of_attackers=self.number_of_attackers,
            number_of_defensers=self.number_of_defensers,
        )
        return map

    def step(self, action):
        reward = list()
        for i in range(self.number_of_attackers + self.number_of_defensers):
            if self.players[i].is_alive():
                res = self.players[i].step(action[i])
                reward.append(res)

        # We are done only when there is no defensers alive an more.
        self.terminated = not all(
            [not defenser.is_alive() for defenser in self.map.get_defensers()]
        )
        self.steps += 1
        return self.map, reward, self.terminated

    def render(self):
        self.rendering.render_map(self.map)

    def kill_the_defenser(self, defenser_position):
        """
        Kills the defenser when touched by an attacker.
        """
        if isinstance(self.map.get_cell(defenser_position), Defenser()):
            self.map.get_cell(defenser_position).kill()
            self.map.assign_element(defenser_position, None)

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

    def close(self):
        pass
