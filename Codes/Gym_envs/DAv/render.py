from typing import List
from Codes.Gym_envs.DAv.players.attacker import Attacker
from Codes.Gym_envs.DAv.players.defenser import Defenser
import time
from Codes.Gym_envs.DAv.map import Map_DAv
from Codes.Gym_envs.DAv.utils.Wall import Wall
import matplotlib.pyplot as plt
import numpy as np

wall_length = 0.5


class Render_DAv:
    def __init__(self):
        plt.ion()
        self.fig = plt.figure()

    def render_env(self, map: Map_DAv):
        ax = self.fig.add_subplot(111)
        plt.xticks(np.arange(0, map.map_size[0], 1))
        plt.yticks(np.arange(0, map.map_size[1], 1))
        plt.grid()
        ax.axis([-1, map.map_size[0], -1, map.map_size[1]])

        self.render_map(map, ax)
        self.render_defensers(map.defensers, ax)
        self.render_attackers(map.attackers, ax)
        self.render_walls(map.walls, ax)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        time.sleep(1)

    def render_map(self, map: Map_DAv, ax):
        ax.plot(map.map_size[0], map.map_size[1])

    def render_defensers(self, defensers: List[Defenser], ax):
        for defenser in defensers:
            ax.scatter(defenser.position[0], defenser.position[1], c=defenser.color)

    def render_attackers(self, attackers: List[Attacker], ax):
        for attacker in attackers:
            ax.scatter(attacker.position[0], attacker.position[1], c=attacker.color)

    def render_walls(self, walls: List[Wall], ax):
        for wall in walls:
            if not wall.is_broken():
                wall_x_pos = wall.get_position()[0]
                wall_y_pos = wall.get_position()[1]
                ax.plot(
                    [wall_x_pos - wall_length, wall_x_pos + wall_length],
                    [wall_y_pos, wall_y_pos],
                    c="peru",
                    label="wall",
                )
                ax.plot(
                    [wall_x_pos, wall_x_pos],
                    [wall_y_pos - wall_length, wall_y_pos + wall_length],
                    c="peru",
                )
