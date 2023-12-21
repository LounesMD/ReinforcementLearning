import pytest

from Codes.Gym_envs.DAv.map import Map_DAv


@pytest.fixture
def example_map():
    """
    Returns a map used to initialized the defender.
    The map is of size (20,20).
    """
    return Map_DAv(number_of_attackers=0, number_of_defenders=1)


@pytest.fixture
def defender_middle(example_map):
    """
    Change the position to the middle of the map so it can be used for tests.
    """
    defender = example_map.get_defenders()[0]
    example_map.change_position(defender.get_position(), (10, 10))
    return defender


@pytest.fixture
def defenders_in_borders():
    """
    Defenders positionned in the corners of the map to test that they can't move beyond the borders of the map.
    """
    map = Map_DAv(number_of_attackers=0, number_of_defenders=2)
    defenders1 = map.get_defenders()[0]
    defenders2 = map.get_defenders()[1]

    map.change_position(defenders1.get_position(), (0, 0))
    map.change_position(defenders2.get_position(), (19, 19))

    return (defenders1, defenders2)


def test_moving_left(defender_middle):
    current_position = defender_middle.get_position()
    defender_middle.step(0)
    new_position = defender_middle.get_position()
    assert new_position == (current_position[0] - 1, current_position[1])


def test_moving_up(defender_middle):
    current_position = defender_middle.get_position()
    defender_middle.step(1)
    new_position = defender_middle.get_position()
    assert new_position == (current_position[0], current_position[1] + 1)


def test_moving_right(defender_middle):
    current_position = defender_middle.get_position()
    defender_middle.step(2)
    new_position = defender_middle.get_position()
    assert new_position == (current_position[0] + 1, current_position[1])


def test_moving_down(defender_middle):
    current_position = defender_middle.get_position()
    defender_middle.step(3)
    new_position = defender_middle.get_position()
    assert new_position == (current_position[0], current_position[1] - 1)


def test_is_alive(defender_middle):
    assert defender_middle.is_alive()


def test_is_dead(defender_middle):
    assert defender_middle.is_alive()
    defender_middle.kill()
    assert not defender_middle.is_alive()


def test_moving_borders(defenders_in_borders):
    defender1 = defenders_in_borders[0]
    defender1_prev_pos = defender1.get_position()

    defender1.step(0)
    defender1_new_pos_left = defender1.get_position()
    assert defender1_new_pos_left == defender1_prev_pos
    defender1.step(3)
    defender1_new_pos_down = defender1.get_position()
    assert defender1_new_pos_down == defender1_prev_pos

    defender2 = defenders_in_borders[1]
    defender2_prev_pos = defender2.get_position()

    defender2.step(1)
    defender2_new_pos_up = defender2.get_position()
    assert defender2_new_pos_up == defender2_prev_pos
    defender2.step(2)
    defender2_new_pos_righ = defender2.get_position()
    assert defender2_new_pos_righ == defender2_prev_pos


def test_reward(defender_middle):
    reward = defender_middle.step(1)
    assert reward == 1 / defender_middle.step_limit
