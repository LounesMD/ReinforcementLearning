import random

import gymnasium as gym
import numpy as np
import pytest

import Codes
from Codes.Mains.Examples.DAv.utils.binary_observation_utils import init_binary_map


@pytest.fixture
def env():
    """
    Returns a DAv environment instantiate using gym.
    """
    env = gym.make("env_DAv-v0", number_of_attackers=2, number_of_defenders=3)
    env.reset()
    return env


def test_binary_map_init_position(env):
    map_size = env.unwrapped.map_size
    binary_map = init_binary_map(
        map_size=map_size,
        attackers=env.unwrapped.attackers,
        defenders=env.unwrapped.defenders,
    )

    for attacker in env.unwrapped.attackers:
        x, y = attacker.get_position()
        assert binary_map.attackers_array[x][y] == 1.0

    for defender in env.unwrapped.defenders:
        x, y = defender.get_position()
        assert binary_map.defenders_array[x][y] == 1.0

    assert np.sum(binary_map.defenders_array) == env.number_of_defenders
    assert np.sum(binary_map.attackers_array) == env.number_of_attackers


def test_binary_map_update_position(env):
    map_size = env.unwrapped.map_size
    binary_map = init_binary_map(
        map_size=map_size,
        attackers=env.unwrapped.attackers,
        defenders=env.unwrapped.defenders,
    )

    attackers_old_positions = list()
    for attacker in env.unwrapped.attackers:
        attackers_old_positions.append(attacker.get_position())
        x, y = attacker.get_position()
        assert binary_map.attackers_array[x][y] == 1.0

    defenders_old_positions = list()
    for defender in env.unwrapped.defenders:
        defenders_old_positions.append(defender.get_position())
        x, y = defender.get_position()
        assert binary_map.defenders_array[x][y] == 1.0

    attackers_new_positions = np.array(
        [
            (random.randint(0, map_size[0] - 1), random.randint(0, map_size[1] - 1))
            for _ in range(len(env.unwrapped.attackers))
        ]
    )
    defenders_new_positions = np.array(
        [
            (random.randint(0, map_size[0] - 1), random.randint(0, map_size[1] - 1))
            for _ in range(len(env.unwrapped.defenders))
        ]
    )

    binary_map.update_observation(
        attackers_position=np.array(attackers_old_positions),
        defenders_position=np.array(defenders_old_positions),
        walls_position=np.array([]),
        new_attackers_position=attackers_new_positions,
        new_defenders_position=defenders_new_positions,
        new_walls_position=np.array([]),
    )

    for i, (x, y) in enumerate(attackers_new_positions):
        assert binary_map.attackers_array[x][y] == 1.0
        if attackers_old_positions[i] != (x, y):
            assert (
                binary_map.attackers_array[attackers_old_positions[i][0]][
                    attackers_old_positions[i][1]
                ]
                == 0.0
            )

    for i, (x, y) in enumerate(defenders_new_positions):
        assert binary_map.defenders_array[x][y] == 1.0
        if defenders_old_positions[i] != (x, y):
            assert (
                binary_map.defenders_array[defenders_old_positions[i][0]][
                    defenders_old_positions[i][1]
                ]
                == 0.0
            )
