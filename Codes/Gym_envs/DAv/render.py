import time
from typing import List

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from Codes.Gym_envs.DAv.map import Map_DAv
from Codes.Gym_envs.DAv.players.attacker import Attacker
from Codes.Gym_envs.DAv.players.defenser import Defenser
from Codes.Gym_envs.DAv.utils.Wall import Wall

wall_length = 0.5


class Render_DAv:
    def __init__(self):
        plt.ion()
        self.fig = plt.figure()

    def render_env(self, map: Map_DAv, steps: int, render_prev_state: bool = True):
        ax = self.fig.add_subplot(111)
        # plt.xticks(np.arange(0, map.map_size[0], 1))
        # plt.yticks(np.arange(0, map.map_size[1], 1))
        # plt.grid()
        self.render_prev_state = render_prev_state
        ax.axis([-1, map.map_size[0], -1, map.map_size[1]])

        self.render_map(map, ax)
        self.render_defensers(map.defensers, ax)
        self.render_attackers(map.attackers, ax)
        self.render_walls(map.walls, ax)

        legend_elements = [
            Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor="red",
                label="Attacker",
                markersize=10,
                linestyle="None",
            ),
            Line2D(
                [0],
                [0],
                marker="o",
                color="w",
                markerfacecolor="green",
                label="Defenser",
                markersize=10,
                linestyle="None",
            ),
            Line2D(
                [0],
                [0],
                marker="+",
                color="w",
                markeredgecolor="peru",
                label="Wall",
                markersize=10,
                linestyle="None",
            ),
        ]

        ax.legend(handles=legend_elements)

        self.fig.suptitle("DAv. Step: " + str(steps))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        # time.sleep(1)

    def render_map(self, map: Map_DAv, ax):
        ax.plot(map.map_size[0], map.map_size[1])

    def render_defensers(self, defensers: List[Defenser], ax):
        for defenser in defensers:
            if self.render_prev_state:
                ax.scatter(defenser.prev_pos[0], defenser.prev_pos[1], c="yellow")
            ax.scatter(defenser.position[0], defenser.position[1], c=defenser.color)

    def render_attackers(self, attackers: List[Attacker], ax):
        for attacker in attackers:
            if self.render_prev_state:
                ax.scatter(attacker.prev_pos[0], attacker.prev_pos[1], c="yellow")
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
                )
                ax.plot(
                    [wall_x_pos, wall_x_pos],
                    [wall_y_pos - wall_length, wall_y_pos + wall_length],
                    c="peru",
                )
