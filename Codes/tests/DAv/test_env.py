import gymnasium as gym
import pytest

import Codes


@pytest.fixture
def env():
    """
    Returns a DAv environment instantiate using gym.
    """
    env = gym.make("env_DAv-v0", number_of_attackers=1, number_of_defensers=1)
    env.reset()
    return env


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


def test_killing_rewards(env_2):
    defenser = env_2.get_map().get_defensers()[0]

    assert defenser.is_alive()
    reward = defenser.step(1)
    assert reward == (1 / defenser.step_limit)

    attacker = env_2.get_map().get_attackers()[0]

    reward = attacker.step(1)
    assert reward == (-1 / attacker.step_limit)
    # Now let's kill the defenser
    reward = attacker.step(1)
    assert reward == 1

    # Let's check that the reward is 0 again
    reward = attacker.step(1)
    assert reward == (-1 / attacker.step_limit)

    assert not defenser.is_alive()
