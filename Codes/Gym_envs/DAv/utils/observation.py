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
    ) -> None:
        super().__init__()
        self.attackers_tensor = attackers_tensor
        self.defensers_tensor = defensers_tensor
        self.walls_tensor = walls_tensor

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

    def observe_attackers_pov(self) -> np.array:
        """
        For the attackers Neural Net, the observation to use is:
        [
            [Binary attackers slice],
            [Binary defensers slice],
            [Binary walls slice],
        ]
        """
        return np.stack(
            (self.attackers_tensor, self.defensers_tensor, self.walls_tensor)
        )

    def observe_defensers_pov(self) -> np.array:
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
