import pytest

from Codes.Gym_envs.DAv.map import Map_DAv
from Codes.Gym_envs.DAv.utils.Wall import Wall


@pytest.fixture
def map_one_defender():
    """
    Returns a map used to initialized the attacker.
    The map is of size (20,20).
    """
    map = Map_DAv(number_of_attackers=0, number_of_defenders=1)
    defender = map.get_defenders()[0]
    map.change_position(defender.get_position(), (10, 10))
    return map


@pytest.fixture
def map_one_defender_one_attacker():
    """
    Returns a map used to initialized the attacker.
    The map is of size (20,20).
    """
    map = Map_DAv(number_of_attackers=1, number_of_defenders=1)
    defender = map.get_defenders()[0]
    map.change_position(defender.get_position(), (10, 10))
    attacker = map.get_attackers()[0]
    map.change_position(attacker.get_position(), (11, 10))
    return map


def test_wall_correctly_drop(map_one_defender):
    defender = map_one_defender.get_defenders()[0]
    current_defender_position = defender.get_position()
    assert defender == map_one_defender.get_cell(current_defender_position)
    assert 0 == map_one_defender.get_cell(
        (current_defender_position[0], current_defender_position[1] + 1)
    )
    defender.step(4)
    assert defender == map_one_defender.get_cell(current_defender_position)
    assert 0 == map_one_defender.get_cell(
        (current_defender_position[0], current_defender_position[1] + 1)
    )
    defender.step(1)

    new_position = (current_defender_position[0], current_defender_position[1] + 1)
    assert isinstance(map_one_defender.get_cell(current_defender_position), Wall)
    assert defender.get_position() == new_position
    assert defender == map_one_defender.get_cell(new_position)


def test_defender_cant_go_through_walls(map_one_defender):
    defender = map_one_defender.get_defenders()[0]
    current_defender_position = defender.get_position()

    assert defender == map_one_defender.get_cell(current_defender_position)
    assert 0 == map_one_defender.get_cell(
        (current_defender_position[0], current_defender_position[1] + 1)
    )
    defender.step(4)
    defender.step(1)

    new_position = (current_defender_position[0], current_defender_position[1] + 1)
    assert defender == map_one_defender.get_cell(new_position)
    assert isinstance(map_one_defender.get_cell(current_defender_position), Wall)

    defender.step(4)
    assert defender == map_one_defender.get_cell(new_position)
    assert isinstance(map_one_defender.get_cell(current_defender_position), Wall)


def test_defender_cant_go_through_walls(map_one_defender_one_attacker):
    defender = map_one_defender_one_attacker.get_defenders()[0]
    attacker = map_one_defender_one_attacker.get_attackers()[0]
    current_defender_position = defender.get_position()
    new_defender_position = (
        current_defender_position[0] - 1,
        current_defender_position[1],
    )

    current_attacker_position = attacker.get_position()
    new_attacker_position = (
        current_attacker_position[0] - 1,
        current_attacker_position[1],
    )

    assert defender == map_one_defender_one_attacker.get_cell(current_defender_position)
    assert defender == map_one_defender_one_attacker.get_cell(new_attacker_position)
    assert attacker == map_one_defender_one_attacker.get_cell(current_attacker_position)
    assert 0 == map_one_defender_one_attacker.get_cell(new_defender_position)

    defender.step(4)
    assert defender == map_one_defender_one_attacker.get_cell(current_defender_position)
    assert defender == map_one_defender_one_attacker.get_cell(new_attacker_position)
    assert attacker == map_one_defender_one_attacker.get_cell(current_attacker_position)
    assert 0 == map_one_defender_one_attacker.get_cell(new_defender_position)

    defender.step(0)
    assert defender == map_one_defender_one_attacker.get_cell(new_defender_position)
    assert attacker == map_one_defender_one_attacker.get_cell(current_attacker_position)
    assert isinstance(
        map_one_defender_one_attacker.get_cell(current_defender_position), Wall
    )

    attacker.step(0)
    assert defender == map_one_defender_one_attacker.get_cell(new_defender_position)
    assert attacker == map_one_defender_one_attacker.get_cell(current_attacker_position)
    assert map_one_defender_one_attacker.get_cell(current_defender_position) == 0

    attacker.step(0)
    assert defender == map_one_defender_one_attacker.get_cell(new_defender_position)
    assert attacker == map_one_defender_one_attacker.get_cell(new_attacker_position)
    assert map_one_defender_one_attacker.get_cell(current_attacker_position) == 0

    attacker.step(0)
    assert attacker == map_one_defender_one_attacker.get_cell(new_attacker_position)
    assert not defender.is_alive()
