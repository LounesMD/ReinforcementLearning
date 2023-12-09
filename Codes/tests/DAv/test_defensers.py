from Codes.Environments.DAv.players.defenser import Defenser
from Codes.Environments.DAv.map import Map_DAv
import pytest

@pytest.fixture
def example_map():
    """
    Returns a map used to initialized the defenser.
    The map is of size (20,20).
    """
    return Map_DAv(number_of_attackers=0, number_of_defensers=1)

@pytest.fixture
def defenser_middle(example_map):
    """
    Change the position to the middle of the map so it can be used for tests.
    """
    defenser = example_map.get_defensers()[0]
    example_map.change_position(defenser.get_position(), (10,10))
    return defenser

@pytest.fixture
def defensers_in_borders():
    """
    Defensers positionned in the corners of the map to test that they can't move beyond the borders of the map.
    """
    map = Map_DAv(number_of_attackers=0, number_of_defensers=2)
    defensers1 = map.get_defensers()[0]
    defensers2 = map.get_defensers()[1]

    map.change_position(defensers1.get_position(), (0,0))
    map.change_position(defensers2.get_position(), (19,19))

    return (defensers1,defensers2)

def test_moving_left(defenser_middle):
    current_position = defenser_middle.get_position()
    defenser_middle.step(0)
    new_position = defenser_middle.get_position()
    assert new_position == (current_position[0]-1 , current_position[1]) 

def test_moving_up(defenser_middle):
    current_position = defenser_middle.get_position()
    defenser_middle.step(1)
    new_position = defenser_middle.get_position()
    assert new_position == (current_position[0] , current_position[1]+1) 

def test_moving_right(defenser_middle):
    current_position = defenser_middle.get_position()
    defenser_middle.step(2)
    new_position = defenser_middle.get_position()
    assert new_position == (current_position[0]+1 , current_position[1]) 

def test_moving_down(defenser_middle):
    current_position = defenser_middle.get_position()
    defenser_middle.step(3)
    new_position = defenser_middle.get_position()
    assert new_position == (current_position[0] , current_position[1]-1) 

def test_is_alive(defenser_middle):
    assert defenser_middle.is_alive()

def test_is_dead(defenser_middle):
    assert defenser_middle.is_alive()
    defenser_middle.kill()
    assert not defenser_middle.is_alive()



def test_moving_borders(defensers_in_borders):
    defenser1 =  defensers_in_borders[0]
    defenser1_prev_pos = defenser1.get_position()

    defenser1.step(0)
    defenser1_new_pos_left = defenser1.get_position()
    assert defenser1_new_pos_left == defenser1_prev_pos
    defenser1.step(3)
    defenser1_new_pos_down = defenser1.get_position()
    assert defenser1_new_pos_down == defenser1_prev_pos


    defenser2 =  defensers_in_borders[1]
    defenser2_prev_pos = defenser2.get_position()

    defenser2.step(1)
    defenser2_new_pos_up = defenser2.get_position()
    assert defenser2_new_pos_up == defenser2_prev_pos
    defenser2.step(2)
    defenser2_new_pos_righ = defenser2.get_position()
    assert defenser2_new_pos_righ == defenser2_prev_pos
