import pytest

from Codes.Gym_envs.DAv.map import Map_DAv
from Codes.Gym_envs.DAv.utils.Wall import Wall


@pytest.fixture
def map_one_defenser():
    """
    Returns a map used to initialized the attacker.
    The map is of size (20,20).
    """
    map = Map_DAv(number_of_attackers=0, number_of_defensers=1)
    defenser = map.get_defensers()[0]
    map.change_position(defenser.get_position(), (10, 10))
    return map


@pytest.fixture
def map_one_defenser_one_attacker():
    """
    Returns a map used to initialized the attacker.
    The map is of size (20,20).
    """
    map = Map_DAv(number_of_attackers=1, number_of_defensers=1)
    defenser = map.get_defensers()[0]
    map.change_position(defenser.get_position(), (10, 10))
    attacker = map.get_attackers()[0]
    map.change_position(attacker.get_position(), (11, 10))
    return map


def test_wall_correctly_drop(map_one_defenser):
    defenser = map_one_defenser.get_defensers()[0]
    current_defenser_position = defenser.get_position()
    assert defenser == map_one_defenser.get_cell(current_defenser_position)
    assert 0 == map_one_defenser.get_cell(
        (current_defenser_position[0], current_defenser_position[1] + 1)
    )
    defenser.step(4)
    assert defenser == map_one_defenser.get_cell(current_defenser_position)
    assert 0 == map_one_defenser.get_cell(
        (current_defenser_position[0], current_defenser_position[1] + 1)
    )
    defenser.step(1)

    new_position = (current_defenser_position[0], current_defenser_position[1] + 1)
    assert isinstance(map_one_defenser.get_cell(current_defenser_position), Wall)
    assert defenser.get_position() == new_position
    assert defenser == map_one_defenser.get_cell(new_position)


def test_defenser_cant_go_through_walls(map_one_defenser):
    defenser = map_one_defenser.get_defensers()[0]
    current_defenser_position = defenser.get_position()

    assert defenser == map_one_defenser.get_cell(current_defenser_position)
    assert 0 == map_one_defenser.get_cell(
        (current_defenser_position[0], current_defenser_position[1] + 1)
    )
    defenser.step(4)
    defenser.step(1)

    new_position = (current_defenser_position[0], current_defenser_position[1] + 1)
    assert defenser == map_one_defenser.get_cell(new_position)
    assert isinstance(map_one_defenser.get_cell(current_defenser_position), Wall)

    defenser.step(4)
    assert defenser == map_one_defenser.get_cell(new_position)
    assert isinstance(map_one_defenser.get_cell(current_defenser_position), Wall)


def test_defenser_cant_go_through_walls(map_one_defenser_one_attacker):
    defenser = map_one_defenser_one_attacker.get_defensers()[0]
    attacker = map_one_defenser_one_attacker.get_attackers()[0]
    current_defenser_position = defenser.get_position()
    new_defenser_position = (
        current_defenser_position[0] - 1,
        current_defenser_position[1],
    )

    current_attacker_position = attacker.get_position()
    new_attacker_position = (
        current_attacker_position[0] - 1,
        current_attacker_position[1],
    )

    assert defenser == map_one_defenser_one_attacker.get_cell(current_defenser_position)
    assert defenser == map_one_defenser_one_attacker.get_cell(new_attacker_position)
    assert attacker == map_one_defenser_one_attacker.get_cell(current_attacker_position)
    assert 0 == map_one_defenser_one_attacker.get_cell(new_defenser_position)

    defenser.step(4)
    assert defenser == map_one_defenser_one_attacker.get_cell(current_defenser_position)
    assert defenser == map_one_defenser_one_attacker.get_cell(new_attacker_position)
    assert attacker == map_one_defenser_one_attacker.get_cell(current_attacker_position)
    assert 0 == map_one_defenser_one_attacker.get_cell(new_defenser_position)

    defenser.step(0)
    assert defenser == map_one_defenser_one_attacker.get_cell(new_defenser_position)
    assert attacker == map_one_defenser_one_attacker.get_cell(current_attacker_position)
    assert isinstance(
        map_one_defenser_one_attacker.get_cell(current_defenser_position), Wall
    )

    attacker.step(0)
    assert defenser == map_one_defenser_one_attacker.get_cell(new_defenser_position)
    assert attacker == map_one_defenser_one_attacker.get_cell(current_attacker_position)
    assert map_one_defenser_one_attacker.get_cell(current_defenser_position) == 0

    attacker.step(0)
    assert defenser == map_one_defenser_one_attacker.get_cell(new_defenser_position)
    assert attacker == map_one_defenser_one_attacker.get_cell(new_attacker_position)
    assert map_one_defenser_one_attacker.get_cell(current_attacker_position) == 0

    attacker.step(0)
    assert attacker == map_one_defenser_one_attacker.get_cell(new_attacker_position)
    assert not defenser.is_alive()
