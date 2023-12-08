from Codes.Environments.Jump_or_Drop_The_Wall.map import Map_JoD
from Codes.Environments.Jump_or_Drop_The_Wall.players.attacker import Attacker
from Codes.Environments.Jump_or_Drop_The_Wall.utils import Wall
from Codes.Environments.Jump_or_Drop_The_Wall.players.defenser import Defenser


class Environment_JoD:
    def __init__(
        self,
        number_of_attackers: int = 2,
        number_of_defensers: int = 2,
        size: tuple = (15,15),
    ) -> None:
        self.map = Map_JoD(
            map_size=size,
            number_of_attackers=number_of_attackers,
            number_of_defensers=number_of_defensers,
        )

    def get_map(self):
        """
        Returns the map used in the environment.
        """
        return self.map

    def kill_the_defenser(self, defenser_position):
        """
        Kills the defenser when touched by an attacker.
        """
        if isinstance(self.map.get_cell(defenser_position), Defenser()):
            self.map.get_cell(defenser_position).kill()
            self.map.assign_element(defenser_position,None)

    def get_defensers(self):
        """
        Returns the defensers of the environment.
        """
        return self.map.get_defensers()

    def get_attackers(self):
        """
        Returns the attackers of the environment.
        """
        return self.map.get_attackers()