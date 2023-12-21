import pytest

from Codes.Gym_envs.DAv.map import Map_DAv


@pytest.fixture
def example_map():
    """
    Returns a map used to initialized the attacker.
    The map is of size (20,20).
    """
    return Map_DAv(number_of_attackers=2, number_of_defenders=3)


@pytest.fixture
def example_map_2():
    """
    Returns a map used to test the echange position method with only one defender.
    """
    return Map_DAv(number_of_attackers=0, number_of_defenders=1)


@pytest.fixture
def map_killer():
    """
    Returns a map used to test that the attacker can indeed kill a defender.
    """
    map = Map_DAv(number_of_attackers=1, number_of_defenders=1)
    attacker = map.get_attackers()[0]
    map.change_position(attacker.get_position(), (0, 0))
    defender = map.get_defenders()[0]
    map.change_position(defender.get_position(), (0, 1))
    return map


@pytest.fixture
def attacker_middle(example_map_2):
    """
    Change the position to the middle of the map so it can be used for tests.
    """
    defender = example_map_2.get_defenders()[0]
    example_map_2.change_position(defender.get_position(), (10, 10))
    return defender


def test_right_number_of_attackers(example_map):
    attackers = example_map.get_attackers()
    assert len(attackers) == 2


def test_right_number_of_defenders(example_map):
    defenders = example_map.get_defenders()
    assert len(defenders) == 3


def test_attackers_well_initialized(example_map):
    for attacker in example_map.get_attackers():
        assert example_map.is_within_limits(attacker.get_position())
        assert example_map == attacker.get_map()
        assert attacker == example_map.get_cell(attacker.get_position())


def test_defenders_well_initialized(example_map):
    for defender in example_map.get_defenders():
        assert example_map.is_within_limits(defender.get_position())
        assert example_map == defender.get_map()
        assert defender == example_map.get_cell(defender.get_position())


def test_is_occupied_by_defender(example_map):
    for defender in example_map.get_defenders():
        example_map.is_occupied_by_defender(defender.get_position())


def test_is_occupied(example_map):
    for defender in example_map.get_defenders():
        example_map.is_occupied(defender.get_position())
    for attacker in example_map.get_attackers():
        example_map.is_occupied(attacker.get_position())


def test_change_position(attacker_middle, example_map_2):
    attacker_pres_pos = attacker_middle.get_position()
    assert example_map_2.get_cell((11, 11)) == 0
    assert example_map_2.get_cell(attacker_pres_pos) == attacker_middle

    example_map_2.change_position(attacker_middle.get_position(), (11, 11))
    attacker_new_pos = attacker_middle.get_position()

    assert example_map_2.get_cell(attacker_pres_pos) == 0
    assert attacker_new_pos == (11, 11)
    assert example_map_2.get_cell(attacker_new_pos) == attacker_middle


def test_kill_a_defender(map_killer):
    for defender in map_killer.get_defenders():
        assert defender.is_alive()

    for attacker in map_killer.get_attackers():
        attacker.step(1)

    for defender in map_killer.get_defenders():
        assert not defender.is_alive()


def test_rewards(map_killer):
    for defender in map_killer.get_defenders():
        assert defender.is_alive()

    for attacker in map_killer.get_attackers():
        reward = attacker.step(1)
    assert reward == 1
