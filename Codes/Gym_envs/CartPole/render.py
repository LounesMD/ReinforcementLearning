import math
import time

import matplotlib.pyplot as plt


class Render_CartPole:
    def __init__(self):
        plt.ion()
        self.fig = plt.figure()

    def render_env(
        self,
        steps: int,
        position: float,
        length: float,
        pole_angle: float,
        savefig: bool = False,
    ):
        ax = self.fig.add_subplot(111)
        ax.set_xlim((-4.8, 4.8))
        ax.set_ylim((-0.5, 1.2))

        x = position
        cart_length = length
        theta = pole_angle

        line1 = ax.scatter([x], [0], marker="s", color="black", label="Cart")

        ax.plot([-2.4, 2.4], [0, 0], color="blue", linewidth=2, label="Track")
        ax.scatter([-2.4, 2.4], [0, 0], color="blue")
        (line2,) = ax.plot(
            [x, x + cart_length * math.sin(theta)],
            [0, cart_length * math.cos(theta)],
            color="brown",
            label="Pole",
        )

        ax.legend()

        self.fig.suptitle(
            "Cart-Pole Environment : Angle "
            + str(round(theta, 4))
            + " Position "
            + str(round(theta, 4))
        )
        if savefig:
            plt.savefig(
                "Cart-Pole Environment : Angle "
                + str(round(theta, 4))
                + " Position "
                + str(round(theta, 4))
            )
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
