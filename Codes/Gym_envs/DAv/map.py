from Codes.Gym_envs.DAv.players.attacker import Attacker
from Codes.Gym_envs.DAv.players.defenser import Defenser
from Codes.Gym_envs.DAv.utils.Wall import Wall

import random
import numpy as np


class Map_DAv:
    """
    The map is composed of a list of lists so we have a matrix that can stored different types: Int, Attacker, Defenser and Wall.
    We do that because np.ndarray doesn't allow this behavior.
    """

    def __init__(
        self,
        map_size: tuple = (20, 20),
        number_of_attackers: int = 1,
        number_of_defensers: int = 1,
    ) -> None:
        self.map_size = map_size
        self.map = self._init_map()  # We instantiate the map with full zeros
        self.attackers = list()
        self.defensers = list()
        self.walls = list()
        self.number_of_attackers = number_of_attackers
        self.number_of_defensers = number_of_defensers
        self._random_init_attackers()
        self._random_init_defensers()

    def _init_map(self):
        return [[0 for i in range(self.map_size[0])] for k in range(self.map_size[1])]

    def get_cell(self, position: tuple):
        """
        Returns the cell at the given position.

        Returns:
            tuple: cell at the positon `positon`
        """
        return self.map[position[0]][position[1]]

    def assign_element(self, position: tuple, element) -> None:
        """Assign to the position `positon` the element `element`

        Args:
            position (tuple): position
            element (_type_): elment that can be Attacker, Defenser or Wall
        """
        self.map[position[0]][position[1]] = element

    def add_wall(self, position):
        # Add a simple wall in the map
        wall = Wall()
        wall.set_position(position)
        self.walls.append(wall)
        self.assign_element(position, wall)

    def remove_wall(self, position):
        # Remove the wall at the given position
        elt = self.get_cell(position)
        if isinstance(elt, Wall):
            self.get_cell(position).break_wall()
            self.assign_element(position, 0)

    def _random_init_attackers(self):
        # We intialize the attackers with a random position
        for _ in range(self.number_of_attackers):
            i, j = random.randint(0, self.map_size[0] - 1), random.randint(
                0, self.map_size[1] - 1
            )
            new_attacker = Attacker(position=(i, j), map=self)
            self.attackers.append(new_attacker)
            if self.map[i][j] == 0:
                self.map[i][j] = new_attacker

    def _random_init_defensers(self):
        # We intialiaze the defensers with a random position
        for _ in range(self.number_of_defensers):
            i, j = random.randint(0, self.map_size[0] - 1), random.randint(
                0, self.map_size[1] - 1
            )
            new_defenser = Defenser(position=(i, j), map=self)
            self.defensers.append(new_defenser)
            if self.map[i][j] == 0:
                self.map[i][j] = new_defenser

    def change_position(self, current_position, new_positon) -> None:
        """
        Move the element at the position 'current_position' to the new position.
        Also, it puts a None in the current position.
        """
        if current_position != new_positon and self.is_accessible(new_positon):
            self.map[new_positon[0]][new_positon[1]] = self.get_cell(current_position)
            self.map[current_position[0]][current_position[1]] = 0
            self.get_cell(new_positon).set_position(new_positon)

    def is_occupied(self, position) -> bool:
        """
        Return True if the cell at the position `position` is occupied by an attacker or a defenser.

        Args:
            position (tuple): position of the cell to check

        Returns:
            Bool: True if occupied and False else
        """
        if isinstance(self.get_cell(position), (Attacker, Defenser)):
            return True
        else:
            return False

    def is_occupied_by_defenser(self, position) -> bool:
        """
        Return True if the cell at the position `position` is occupied by a defenser.
        This method is used by the attacker to know if it has to kill a defenser or not.
        Args:
            position (tuple): position of the cell to check

        Returns:
            Bool: True if occupied and False else
        """
        if isinstance(self.get_cell(position), Defenser):
            return True
        else:
            return False

    def is_within_limits(self, position) -> bool:
        """ "
        Returns True if the position is within the dimension of of the map.
        """
        ok_in_x = 0 <= position[0] < self.map_size[1]
        ok_in_y = 0 <= position[1] < self.map_size[1]
        return ok_in_x and ok_in_y

    def is_blocked(self, position) -> bool:
        """
        Returns True if the position in not accessible because of a Wall.
        """
        return self.is_within_limits(position) and isinstance(
            self.get_cell(position), Wall
        )

    def is_accessible(self, position) -> bool:
        """
        Test if the cell at the input position is available or not.

        Args:
            position (tuple): Cell's position to test.

        Returns:
            bool: True if the cell is available and False else.

        """
        # TODO: Find a way to do the evaluation in cascade
        if self.is_within_limits(position=position):
            if not self.is_occupied(position=position):
                if not self.is_blocked(position=position):
                    return True
                return False
            return False
        return False

    def get_defensers(self):
        """
        Returns a list of the defensers positionned in the map.
        """
        return self.defensers

    def get_attackers(self):
        """
        Returns a list of the attackers positionned in the map.
        """
        return self.attackers

    def get_walls(self):
        """
        Returns a list of the walls in the map.
        """
        return self.walls