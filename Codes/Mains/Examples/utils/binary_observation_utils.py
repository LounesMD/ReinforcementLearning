import numpy as np


class ObservationType(object):
    def __init__(self) -> None:
        pass


class BinaryMapObservation(ObservationType):
    """
    This class implements the binary reprensentation of DAv.
    With this class we can get a binary representation for the attackers point of view:
        - Slice 1: array of size map_size with 0 every where and 1 at the position of the current attacker
        - Slice 2: array of size map_size with 0 every where and 1 at the position of the current attackers
        - Slice 3: array of size map_size with 0 every where and 1 at the position of the defensers
        - Slice 4: array of size map_size with 0 every where and 1 at the position of the walls
    Or for the defensers point of view:
        - Slice 1: array of size map_size with 0 every where and 1 at the position of the current defenser
        - Slice 2: array of size map_size with 0 every where and 1 at the position of the current defensers
        - Slice 3: array of size map_size with 0 every where and 1 at the position of the attackers
        - Slice 4: array of size map_size with 0 every where and 1 at the position of the walls

    The slices are np.array and the an observation is a np.stack of np.array.
    """

    def __init__(
        self,
        attackers_array: np.array,
        defensers_array: np.array,
        walls_array: np.array,
        map_size: tuple,
    ) -> None:
        super().__init__()
        self.attackers_array = attackers_array
        self.defensers_array = defensers_array
        self.walls_array = walls_array
        self.map_size = map_size

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
        return np.stack((self.attackers_array, self.defensers_array, self.walls_array))

    def defensers_pov(self) -> np.array:
        """
        For the defensers Neural Net, the observation to use is:
        [
            [Binary defensers slice],
            [Binary attackers slice],
            [Binary walls slice],
        ]
        """
        return np.stack((self.defensers_array, self.attackers_array, self.walls_array))

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
        current_attacker_slice = np.zeros(
            shape=(self.map_size[0], self.map_size[1]), dtype=np.float32
        )
        current_attacker_slice[attacker_position[0]][attacker_position[1]] = 1.0
        return np.stack(
            (
                current_attacker_slice,
                self.attackers_array,
                self.defensers_array,
                self.walls_array,
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
        current_defenser_slice = np.zeros(
            shape=(self.map_size[0], self.map_size[1]), dtype=np.float32
        )
        current_defenser_slice[defenser_position[0]][defenser_position[1]] = 1.0
        return np.stack(
            (
                current_defenser_slice,
                self.defensers_array,
                self.attackers_array,
                self.walls_array,
            )
        )

    def update_observation(
        self,
        attackers_position,
        defensers_position,
        walls_position,
        new_attackers_position,
        new_defensers_position,
        new_walls_position,
    ):
        """
        Update the positions of the attackers, defensers and walls with new positions.
        """
        # Update attackers array
        self.attackers_array[attackers_position[:, 0], attackers_position[:, 1]] = 0.0
        self.attackers_array[
            new_attackers_position[:, 0], new_attackers_position[:, 1]
        ] = 1.0
        # Update defensers array
        if np.any(defensers_position):
            self.defensers_array[
                defensers_position[:, 0], defensers_position[:, 1]
            ] = 0.0
        if np.any(new_defensers_position):
            self.defensers_array[
                new_defensers_position[:, 0], new_defensers_position[:, 1]
            ] = 1.0
        # Update walls array
        if np.any(walls_position):
            self.walls_array[walls_position[:, 0], walls_position[:, 1]] = 0.0
        if np.any(new_walls_position):
            self.walls_array[new_walls_position[:, 0], new_walls_position[:, 1]] = 1.0


def init_binary_map(map_size, attackers, defensers) -> list:
    """
    This method initializes a binary map of a DAv environment.
    Args:
        map_size (tuple): size of the input map. Ex: (20,20).
        attackers (list): List of the attackers of the map. Ex: [Attacker1, Attacker2]
        defensers (list): List of the defensers of the map. Ex: [Defensers1, Defensers2]

    Output:
        BinaryMapObservation: A binary map representation of the input:
            - Slice x: array of size map_size with 0 every where and 1 at the position of the attackers
            - Slice y: array of size map_size with 0 every where and 1 at the position of the defensers
            - Slice z: array of size map_size with 0 every where and 1 at the position of the walls
    """
    walls_tensor = np.zeros(
        shape=(map_size[0], map_size[1]), dtype=np.float32
    )  # At the initialisation, there is no wall.

    # Initialisation of the attackers position
    attackers_tensor = np.zeros(shape=(map_size[0], map_size[1]), dtype=np.float32)
    for attacker in attackers:
        attackers_tensor[attacker.get_position()[0]][attacker.get_position()[1]] = 1.0

    # Initialisation of the defensers position
    defensers_tensor = np.zeros(shape=(map_size[0], map_size[1]), dtype=np.float32)
    for defenser in defensers:
        defensers_tensor[defenser.get_position()[0]][defenser.get_position()[1]] = 1.0

    return BinaryMapObservation(
        attackers_tensor, defensers_tensor, walls_tensor, map_size
    )
