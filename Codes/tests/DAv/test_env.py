import gymnasium as gym
import pytest
import Codes


@pytest.fixture
def env():
    """
    Returns a DAv environment instantiate using gym.
    """
    return gym.make("env_DAv-v0")


def test_check_right_correspondance_binary_map(env):
    binary_map = env.binary_map

    for attacker in env.attackers:
        assert (
            binary_map.get_attackers_tensor()[attacker.get_position()[0]][
                attacker.get_position()[1]
            ]
            == 1.0
        )
    for defenser in env.defensers:
        assert (
            binary_map.get_defensers_tensor()[defenser.get_position()[0]][
                defenser.get_position()[1]
            ]
            == 1.0
        )


def test_kill_defenser(env):
    for defenser in env.defensers:
        assert (
            env.binary_map.get_defensers_tensor()[defenser.get_position()[0]][
                defenser.get_position()[1]
            ]
            == 1.0
        )
        env.kill_the_defenser(defenser.get_position())
        assert (
            env.binary_map.get_defensers_tensor()[defenser.get_position()[0]][
                defenser.get_position()[1]
            ]
            == 0.0
        )
