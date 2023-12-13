import numpy as np


class ObservationType(object):
    def __init__(self) -> None:
        pass


class BinaryMapObservation(ObservationType):
    def __init__(
        self,
        attackers_tensor: np.array,
        defensers_tensor: np.array,
        walls_tensor: np.array,
        map_size: tuple,
    ) -> None:
        super().__init__()
        self.attackers_tensor = attackers_tensor
        self.defensers_tensor = defensers_tensor
        self.walls_tensor = walls_tensor
        self.map_size = map_size

    def get_attackers_tensor(self) -> np.array:
        return self.attackers_tensor

    def update_attackers_tensor(self, position, element) -> None:
        self.attackers_tensor[position[0]][position[1]] = element

    def get_defensers_tensor(self) -> np.array:
        return self.defensers_tensor

    def update_defensers_tensor(self, position, element) -> None:
        self.defensers_tensor[position[0]][position[1]] = element

    def get_walls_tensor(self) -> np.array:
        return self.walls_tensor

    def update_walls_tensor(self, position, element) -> None:
        self.walls_tensor[position[0]][position[1]] = element

    def attackers_pov(self) -> np.array:
        """
        For the attackers Neural Net, the observation to use is:
        [
            [Binary current attacker slice],
            [Binary attackers slice],
            [Binary defensers slice],
            [Binary walls slice],
        ]
        """
        return np.stack(
            (self.attackers_tensor, self.defensers_tensor, self.walls_tensor)
        )

    def defensers_pov(self) -> np.array:
        """
        For the defensers Neural Net, the observation to use is:
        [
            [Binary defensers slice],
            [Binary attackers slice],
            [Binary walls slice],
        ]
        """
        return np.stack(
            (self.defensers_tensor, self.attackers_tensor, self.walls_tensor)
        )

    def nn_attackers_pov(self, attacker_position) -> np.array:
        """
        For the attackers Neural Net, the observation to use is:
        [
            [Binary current attacker slice],
            [Binary attackers slice],
            [Binary defensers slice],
            [Binary walls slice],
        ]
        """
        current_attacker_slice = np.zeros(shape=(self.map_size[0], self.map_size[1]))
        current_attacker_slice[attacker_position[0]][attacker_position[1]] = 1.0
        return np.stack(
            (
                current_attacker_slice,
                self.attackers_tensor,
                self.defensers_tensor,
                self.walls_tensor,
            )
        )

    def nn_defensers_pov(self, defenser_position) -> np.array:
        """
        For the defensers Neural Net, the observation to use is:
        [
            [Binary current defenser slice],
            [Binary defensers slice],
            [Binary attackers slice],
            [Binary walls slice],
        ]
        """
        current_defenser_slice = np.zeros(shape=(self.map_size[0], self.map_size[1]))
        current_defenser_slice[defenser_position[0]][defenser_position[1]] = 1.0
        return np.stack(
            (
                current_defenser_slice,
                self.defensers_tensor,
                self.attackers_tensor,
                self.walls_tensor,
            )
        )
