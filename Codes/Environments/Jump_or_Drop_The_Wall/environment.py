from Codes.Environments.Jump_or_Drop_The_Wall.map import Map
from Codes.Environments.Jump_or_Drop_The_Wall.players.attacker import Attacker
import random
from Codes.Environments.Jump_or_Drop_The_Wall.utils import Wall

from Environments.Jump_or_Drop_The_Wall.players.defenser import Defenser


class Environment_JoD:
    def __init__(
        self,
        number_of_attackers: int = 1,
        number_of_defensers: int = 1,
        size: tuple = (20, 20),
    ) -> None:
        self.map = Map(
            map_size=size,
            number_of_attackers=number_of_attackers,
            number_of_defensers=number_of_defensers,
        )

    def add_wall(self, position):
        # Add a simple wall in the map
        if self.map.get_cell(position=position) is None:
            self.map.assign_element(position, Wall())

    def remove_wall(self, position):
        # Remove the wall at the given position
        if isinstance(self.map.get_cell(position), Wall):
            self.map.assign_element(position, None)
        else:
            raise Exception("No wall here")

    def get_map(self):
        return self.map

    def kill_the_defenser(self, defenser_position):
        if isinstance(self.map.get_cell(defenser_position), Defenser()):
            self.map.get_cell(defenser_position).kill()

    def change_position(self, current_position, new_positon) -> None:
        if current_position != new_positon and self.is_accessible(new_positon):
            self.map

    def is_occupied(self, position) -> bool:
        """
        Return True if the cell at the position `position` is occupied by an attacker or a defenser.

        Args:
            position (tuple): position of the cell to check

        Returns:
            Bool: True if occupied and False else
        """
        if isinstance(self.map[position[0]][position[1]], (Attacker, Defenser)):
            return True
        else:
            return False

    def is_within_limits(self, position) -> bool:
        return True

    def is_accessible(self, position) -> bool:
        """
        Test if the cell at the input position is available or not.

        Args:
            position (tuple): Cell's position to test.

        Returns:
            bool: True if the cell is available and False else.
        """
        return not (
            self.is_occupied(position=position)
            and self.is_within_limits(position=position)
        )
