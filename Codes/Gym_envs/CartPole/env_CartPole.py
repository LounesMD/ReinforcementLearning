import math
import random
from typing import List, Tuple

import gymnasium as gym
import numpy as np
from matplotlib import pyplot as plt

from Codes.Gym_envs.CartPole.render import Render_CartPole


class Env_CartPole(gym.Env):
    """
    Gymnasium version of the CartPole environment, a classic reinforcement learning problem.

    The CartPole environment simulates a pole standing upright on a moving cart. The goal is
    to balance the pole by applying forces to the cart. The problem is considered as solved
    if the pole remains upright for a predefined number of time steps.

    Attributes:
    - action_space (gym.spaces.Discrete): The discrete action space (2 actions: 0 or 1).
    - observation_space (gym.spaces.Sequence): The observation space of the environment.
    - steps (int): The current number of steps taken in the environment.
    - step_limit (int): The limit of steps after which the episode is truncated.
    - gravity, mass_cart, mass_pole, length, force_mag, tau: Physical parameters of the environment.
    - min_position, max_position, min_velocity, max_velocity: Bounds for the cart's position and velocity.
    - min_pole_angle, max_pole_angle, min_pole_angular_velocity, max_pole_angular_velocity: Bounds for the pole's angle and angular velocity.

    The class includes methods to initialize the environment, reset it to a starting state,
    advance the state based on an action, and check for terminal or truncated states.

    References:
    - https://coneural.org/florian/papers/05_cart_pole.pdf
    - https://ieeexplore.ieee.org/document/6313077

    Parameters for initialization:
    - gravity (float): The gravitational constant.
    - mass_cart (float): The mass of the cart.
    - mass_pole (float): The mass of the pole.
    - pole_length (float): The length of the pole.
    - force_mag (float): The magnitude of the force to apply to the cart.
    - tau (float): The time step for the environment.
    - min_position, max_position, min_velocity, max_velocity, min_pole_angle, max_pole_angle,
      min_pole_angular_velocity, max_pole_angular_velocity: The minimum and maximum bounds
      for the cart and pole properties.
    - step_limit (int): The maximum number of steps per episode.
    """

    def __init__(
        self,
        gravity: float = 9.8,
        mass_cart: float = 1.0,
        mass_pole: float = 0.1,
        pole_length: float = 0.5,
        force_mag: float = 10.0,
        tau: float = 0.02,
        min_position: float = -0.05,
        max_position: float = 0.05,
        min_velocity: float = -0.05,
        max_velocity: float = 0.05,
        min_pole_angle: float = -0.05,
        max_pole_angle: float = 0.05,
        min_pole_angular_velocity: float = -0.05,
        max_pole_angular_velocity: float = 0.05,
        step_limit: int = 500,
        rendering: bool = True,
    ):
        self.action_space = gym.spaces.Discrete(2)
        # TODO: fix the observation_space.
        self.observation_space = gym.spaces.Sequence(gym.spaces.Box(low=-5, high=5))
        self.steps = 0
        self.step_limit = step_limit
        self.gravity = gravity
        self.mass_cart = mass_cart
        self.mass_pole = mass_pole
        self.total_mass = self.mass_pole + self.mass_cart
        self.length = pole_length
        self.pole_mass_length = self.mass_pole * self.length
        self.force_mag = force_mag
        self.tau = tau
        self.min_position = min_position
        self.max_position = max_position
        self.min_velocity = min_velocity
        self.max_velocity = max_velocity
        self.min_pole_angle = min_pole_angle
        self.max_pole_angle = max_pole_angle
        self.min_pole_angular_velocity = min_pole_angular_velocity
        self.max_pole_angular_velocity = max_pole_angular_velocity
        if rendering:
            self.rendering = Render_CartPole()
        self.terminated = False
        self.truncated = False
        self.steps = None
        self.position = None
        self.velocity = None
        self.pole_angle = None
        self.pole_angular_velocity = None
        self.reset()

    def step(self, action) -> Tuple[List, int, bool, bool, dict]:
        """
        Advances the state of the cart by one step based on the given action.

        The method updates the attributes 'steps', 'position', 'velocity', 'pole_angle',
        and 'pole_angular_velocity' based on the specified action (either 0 or 1) and
        the current state of the object. It uses a semi-implicit Euler method for the
        numerical integration to update these values.

        Parameters:
        - action: An integer (0 or 1) representing the action to be taken.

        Returns:
        - A tuple containing:
            - A list representing the current observation of the state.
            - An integer reward for the action taken.
            - A boolean indicating if the current state is a terminal state.
            - A boolean indicating if the step limit has been reached (truncation).
            - A dictionary with additional information (empty in the current implementation).

        The method asserts that the action must be either 0 or 1. It applies forces
        based on the action, computes new states using physical equations, and then
        checks if the new state is terminal or truncated.
        """
        assert action == 0 or action == 1
        self.steps += 1
        force = self.force_mag if action == 1 else -self.force_mag
        costheta = math.cos(self.pole_angle)
        sintheta = math.sin(self.pole_angle)

        temp = (
            force + self.pole_mass_length * (self.pole_angular_velocity) ** 2 * sintheta
        ) / self.total_mass

        thetaacc = (self.gravity * sintheta - costheta * temp) / (
            self.length * (4.0 / 3.0 - self.mass_pole * costheta**2 / self.total_mass)
        )

        xacc = temp - self.pole_mass_length * thetaacc * costheta / self.total_mass

        # Semi implicit Euler
        self.velocity += self.tau * xacc
        self.position += self.tau * self.velocity
        self.pole_angular_velocity += self.tau * thetaacc
        self.pole_angle += self.tau * self.pole_angular_velocity

        self._bound()
        self.terminated = self._final_state()
        self.truncated = self.steps >= self.step_limit
        reward = 1
        info = dict()  # No info for the moment.
        return self._get_obs(), reward, self.terminated, self.truncated, info

    def render(self):
        """
        Render the environment using matplotlib.
        """
        self.rendering.render_env(
            steps=self.steps,
            position=self.position,
            length=self.length,
            pole_angle=self.pole_angle,
        )

    def reset(self, seed=None, options=None) -> None:
        """
        Resets the attributes of the object to a random state within specified bounds.

        This method initializes the 'steps' attribute to 0 and randomly sets the
        'position', 'velocity', 'pole_angle', and 'pole_angular_velocity' attributes
        within their respective minimum and maximum bounds. These bounds are defined
        by the 'min_position', 'max_position', 'min_velocity', 'max_velocity',
        'min_pole_angle', 'max_pole_angle', 'min_pole_angular_velocity', and
        'max_pole_angular_velocity' attributes of the object.

        Parameters:
        - seed (optional): A seed value for the random number generator.
        - options (optional): Additional options for resetting (not used in the current implementation).

        The method does not return any value.
        """
        self.steps = 0
        self.position = random.uniform(self.min_position, self.max_position)
        self.velocity = random.uniform(self.min_velocity, self.max_velocity)
        self.pole_angle = random.uniform(self.min_pole_angle, self.max_pole_angle)
        self.pole_angular_velocity = random.uniform(
            self.min_pole_angular_velocity, self.max_pole_angular_velocity
        )
        self.terminated = False
        self.truncated = False

    def _final_state(self) -> bool:
        """
        Checks if the current state meets the criteria for being considered a final state.

        The method returns True if any of the following conditions are met:
        - The 'pole_angle' is greater than or equal to 12 * 2 * math.pi / 360.
        - The 'pole_angle' is less than or equal to -12 * 2 * math.pi / 360.
        - The 'position' is greater than or equal to 2.4.
        - The 'position' is less than or equal to -2.4.

        Otherwise, it returns False, indicating that the current state is not a final state.
        """
        return (
            self.pole_angle >= (12 * 2 * math.pi / 360)
            or self.pole_angle <= -(12 * 2 * math.pi / 360)
            or self.position >= 2.4
            or self.position <= -2.4
        )

    def _bound(self) -> None:
        """
        Ensures that the 'position' and 'pole_angle' attributes of the cart
        stay within predefined bounds.

        The method sets the 'position' attribute to -4.8 or 4.8 if it falls outside
        the range [-4.8, 4.8]. Similarly, it adjusts the 'pole_angle' attribute to
        stay within the range [-12 * 4 * math.pi / 360, 12 * 4 * math.pi / 360].
        """
        if self.position < -4.8:
            self.position = -4.8
        elif self.position > 4.8:
            self.position = 4.8

        if self.pole_angle < -(12 * 4 * math.pi / 360):
            self.pole_angle = -(12 * 4 * math.pi / 360)
        elif self.pole_angle > 12 * 4 * math.pi / 360:
            self.pole_angle = 12 * 4 * math.pi / 360

    def _get_obs(self) -> List:
        """
        Returns the observation of the current state of the cart.
        The observation is composed of:
            position (float): x position of the cart.
            velocity (float): velocity of the cart.
            pole_angle (float): angle of the pole.
            pole_angular_velocity (float): angular velocity of the cart.
        """
        return [
            self.position,
            self.velocity,
            self.pole_angle,
            self.pole_angular_velocity,
        ]

    def get_possible_actions(self) -> List:
        """
        Returns a list with the legal actions of the cart.
        """
        return [0, 1]


class CartPoleDiscretizer:
    def __init__(
        self, bins=(20, 20, 20, 20)
    ):  # You can change the number of bins based on your requirements
        self.bins = bins
        self.lowerBounds = [-4.8, -3, -(12 * 2 * math.pi / 360), -10]
        self.upperBounds = [4.8, 3, (12 * 4 * math.pi / 360), 10]

    def discretize(self, state):
        position = state[0]
        velocity = state[1]
        angle = state[2]
        angularVelocity = state[3]

        cartPositionBin = np.linspace(
            self.lowerBounds[0], self.upperBounds[0], self.bins[0]
        )
        cartVelocityBin = np.linspace(
            self.lowerBounds[1], self.upperBounds[1], self.bins[1]
        )
        poleAngleBin = np.linspace(
            self.lowerBounds[2], self.upperBounds[2], self.bins[2]
        )
        poleAngleVelocityBin = np.linspace(
            self.lowerBounds[3], self.upperBounds[3], self.bins[3]
        )

        indexPosition = np.maximum(np.digitize(state[0], cartPositionBin) - 1, 0)
        indexVelocity = np.maximum(np.digitize(state[1], cartVelocityBin) - 1, 0)
        indexAngle = np.maximum(np.digitize(state[2], poleAngleBin) - 1, 0)
        indexAngularVelocity = np.maximum(
            np.digitize(state[3], poleAngleVelocityBin) - 1, 0
        )

        return tuple([indexPosition, indexVelocity, indexAngle, indexAngularVelocity])
