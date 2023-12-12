from Codes.Gym_envs.DAv.players.attacker import Attacker
from Codes.Gym_envs.DAv.players.defenser import Defenser
import gymnasium as gym
import pytest
import random
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


def test_binary_map_update(env):
    def_pos = list()
    att_pos = list()

    for defenser in env.defensers:
        current_pos_def = defenser.get_position()
        def_pos.append(current_pos_def)
        assert (
            env.binary_map.get_defensers_tensor()[current_pos_def[0]][
                current_pos_def[1]
            ]
            == 1.0
        )
        assert isinstance(env.get_map().get_cell(current_pos_def), Defenser)

    for attacker in env.attackers:
        current_pos_att = attacker.get_position()
        att_pos.append(current_pos_att)
        assert (
            env.binary_map.get_attackers_tensor()[current_pos_att[0]][
                current_pos_att[1]
            ]
            == 1.0
        )
        assert isinstance(env.get_map().get_cell(current_pos_att), Attacker)

    actions = [random.choice([0, 1, 2, 3]) for _ in range(4)]
    _, rewards, _, _, _ = env.step(actions)

    for i, defenser in enumerate(env.defensers):
        current_pos_def = def_pos[i]
        new_pos = defenser.get_position()
        if new_pos != current_pos_def:
            assert env.binary_map.get_defensers_tensor()[new_pos[0]][new_pos[1]] == 1.0
            assert isinstance(env.get_map().get_cell(new_pos), Defenser)

        else:
            assert (
                env.binary_map.get_defensers_tensor()[current_pos_def[0]][
                    current_pos_def[1]
                ]
                == 1.0
            )
            assert env.binary_map.get_defensers_tensor()[new_pos[0]][new_pos[1]] == 1.0
            assert isinstance(env.get_map().get_cell(current_pos_def), Defenser)
            assert isinstance(env.get_map().get_cell(new_pos), Defenser)

    for i, attacker in enumerate(env.attackers):
        new_pos = attacker.get_position()
        current_pos_att = att_pos[i]
        if new_pos != current_pos_att:
            assert env.binary_map.get_attackers_tensor()[new_pos[0]][new_pos[1]] == 1.0
            assert isinstance(env.get_map().get_cell(new_pos), Attacker)

        else:
            assert (
                env.binary_map.get_attackers_tensor()[current_pos_att[0]][
                    current_pos_att[1]
                ]
                == 1.0
            )
            assert env.binary_map.get_attackers_tensor()[new_pos[0]][new_pos[1]] == 1.0
            assert isinstance(env.get_map().get_cell(current_pos_att), Attacker)
            assert isinstance(env.get_map().get_cell(new_pos), Attacker)

    cpt = 0
    for defenser in env.defensers:
        if defenser.is_alive():
            cpt += 1
    assert rewards[1] == cpt
    assert rewards[0] == env.number_of_defensers - cpt
