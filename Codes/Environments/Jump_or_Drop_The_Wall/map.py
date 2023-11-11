import random

from Codes.Environments.Jump_or_Drop_The_Wall.players.attacker import Attacker
from Codes.Environments.Jump_or_Drop_The_Wall.players.defenser import Defenser


class Map:
    def __init__(
        self,
        map_size: tuple,
        number_of_attackers: int = 1,
        number_of_defensers: int = 1,
    ) -> None:
        self.map = dict()
        self.map_size = map_size
        self._init_map()
        self._random_init_attackers()
        self._random_init_defensers()
        self.attackers = list()
        self.defensers = list()
        self.number_of_attackers = number_of_attackers
        self.number_of_densers = number_of_defensers

    def _init_map(self):
        """
        Initialize the dictionnary that represents the map.
        TODO(): Change the way the map is defined. I plan to do something much more Object Oriented.
        """
        for i in range(self.map_size[0]):
            self.map[i] = dict()
            for j in range(self.map_size[1]):
                self.map[i][j] = None

    def _random_init_attackers(self):
        # We intialize the attackers with a random position
        for nb in range(self.number_of_attackers):
            i, j = random.randint(0, self.map_size[0]), random.randint(
                0, self.map_size[0]
            )
            new_attacker = Attacker(position=(i, j), env=self)
            self.attackers.append(new_attacker)
            if self.map[i][j] == None:
                self.map[i][j] = new_attacker

    def _random_init_defenser(self):
        # We intialiaze the defensers with a random position
        for nb in range(self.number_of_defensers):
            i, j = random.randint(0, self.map_size[0]), random.randint(
                0, self.map_size[0]
            )
            new_defenser = Defenser(position=(i, j), env=self)
            self.attackers.append(new_defenser)
            if self.map[i][j] == None:
                self.map[i][j] = new_defenser

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
