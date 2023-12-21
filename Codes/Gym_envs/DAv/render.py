import time
from typing import List

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from Codes.Gym_envs.DAv.map import Map_DAv
from Codes.Gym_envs.DAv.players.attacker import Attacker
from Codes.Gym_envs.DAv.players.defender import Defender
from Codes.Gym_envs.DAv.utils.Wall import Wall

wall_length = 0.5


class Render_DAv:
    def __init__(self):
        plt.ion()
        self.fig = plt.figure()

    def render_env(
        self,
        map: Map_DAv,
        steps: int,
        render_prev_state: bool = True,
        savefig: bool = False,
    ):
        ax = self.fig.add_subplot(111)
        self.render_prev_state = render_prev_state
        ax.axis([-1, map.map_size[0], -1, map.map_size[1]])

        self.render_map(map, ax)
        self.render_defenders(map.defenders, ax)
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
                label="Defender",
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

        ax.legend(handles=legend_elements, loc="upper right")

        self.fig.suptitle("DAv. Step: " + str(steps))
        if savefig:
            plt.savefig("DAv. step: " + str(steps) + ".png")
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        # time.sleep(3)

    def render_map(self, map: Map_DAv, ax):
        ax.plot(map.map_size[0], map.map_size[1])

    def render_defenders(self, defenders: List[Defender], ax):
        for defender in defenders:
            if self.render_prev_state:
                ax.scatter(defender.prev_pos[0], defender.prev_pos[1], c="yellow")
            ax.scatter(defender.position[0], defender.position[1], c=defender.color)

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
