import gymnasium as gym
import pytest
import Codes


@pytest.fixture
def env():
    """
    Returns a DAv environment instantiate using gym.
    """
    return gym.make("env_DAv-v0")


@pytest.fixture
def env_2():
    """
    Returns a DAv environment instantiate using gym.
    """
    DAv_env = gym.make("env_DAv-v0")
    attacker = DAv_env.get_map().get_attackers()[0]
    DAv_env.get_map().change_position(attacker.get_position(), (0, 0))
    defenser = DAv_env.get_map().get_defensers()[0]
    DAv_env.get_map().change_position(defenser.get_position(), (0, 1))
    return DAv_env


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


def test_killing_rewards(env_2):
    defenser = env_2.get_map().get_defensers()[0]

    assert defenser.is_alive()
    reward = defenser.step(1)
    assert reward == 1

    attacker = env_2.get_map().get_attackers()[0]

    reward = attacker.step(1)
    assert reward == 0
    # Now let's kill the defenser
    reward = attacker.step(1)
    assert reward == 1

    # Let's check that the reward is 0 again
    reward = attacker.step(1)
    assert reward == 0

    assert not defenser.is_alive()
