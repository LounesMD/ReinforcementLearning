import pytest

from Codes.Gym_envs.DAv.map import Map_DAv


@pytest.fixture
def example_map():
    """
    Returns a map used to initialized the attacker.
    The map is of size (20,20).
    """
    return Map_DAv(number_of_attackers=1, number_of_defenders=0)


@pytest.fixture
def attacker_middle(example_map):
    """
    Change the position to the middle of the map so it can be used for tests.
    """
    attacker = example_map.get_attackers()[0]
    example_map.change_position(attacker.get_position(), (10, 10))
    return attacker


@pytest.fixture
def attackers_in_borders():
    """
    Attackers positionned in the corners of the map to test that they can't move beyond the borders of the map.
    """
    map = Map_DAv(number_of_attackers=2, number_of_defenders=0)
    attacker1 = map.get_attackers()[0]
    attacker2 = map.get_attackers()[1]

    map.change_position(attacker1.get_position(), (0, 0))
    map.change_position(attacker2.get_position(), (19, 19))

    return (attacker1, attacker2)


def test_moving_left(attacker_middle):
    current_position = attacker_middle.get_position()
    attacker_middle.step(0)
    new_position = attacker_middle.get_position()
    assert new_position == (current_position[0] - 1, current_position[1])


def test_moving_up(attacker_middle):
    current_position = attacker_middle.get_position()
    attacker_middle.step(1)
    new_position = attacker_middle.get_position()
    assert new_position == (current_position[0], current_position[1] + 1)


def test_moving_right(attacker_middle):
    current_position = attacker_middle.get_position()
    attacker_middle.step(2)
    new_position = attacker_middle.get_position()
    assert new_position == (current_position[0] + 1, current_position[1])


def test_moving_down(attacker_middle):
    current_position = attacker_middle.get_position()
    attacker_middle.step(3)
    new_position = attacker_middle.get_position()
    assert new_position == (current_position[0], current_position[1] - 1)


def test_moving_borders(attackers_in_borders):
    attacker1 = attackers_in_borders[0]
    attacker1_prev_pos = attacker1.get_position()

    attacker1.step(0)
    attacker1_new_pos_left = attacker1.get_position()
    assert attacker1_new_pos_left == attacker1_prev_pos
    attacker1.step(3)
    attacker1_new_pos_down = attacker1.get_position()
    assert attacker1_new_pos_down == attacker1_prev_pos

    attacker2 = attackers_in_borders[1]
    attacker2_prev_pos = attacker2.get_position()

    attacker2.step(1)
    attacker2_new_pos_up = attacker2.get_position()
    assert attacker2_new_pos_up == attacker2_prev_pos
    attacker2.step(2)
    attacker2_new_pos_righ = attacker2.get_position()
    assert attacker2_new_pos_righ == attacker2_prev_pos


def test_reward(attacker_middle):
    reward = attacker_middle.step(1)
    assert reward == -1 / attacker_middle.step_limit
