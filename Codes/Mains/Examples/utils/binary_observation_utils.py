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
        - Slice 3: array of size map_size with 0 every where and 1 at the position of the defenders
        - Slice 4: array of size map_size with 0 every where and 1 at the position of the walls
    Or for the defenders point of view:
        - Slice 1: array of size map_size with 0 every where and 1 at the position of the current defender
        - Slice 2: array of size map_size with 0 every where and 1 at the position of the current defenders
        - Slice 3: array of size map_size with 0 every where and 1 at the position of the attackers
        - Slice 4: array of size map_size with 0 every where and 1 at the position of the walls

    The slices are np.array and the an observation is a np.stack of np.array.
    """

    def __init__(
        self,
        attackers_array: np.array,
        defenders_array: np.array,
        walls_array: np.array,
        map_size: tuple,
    ) -> None:
        super().__init__()
        self.attackers_array = attackers_array
        self.defenders_array = defenders_array
        self.walls_array = walls_array
        self.map_size = map_size

    def attackers_pov(self) -> np.array:
        """
        For the attackers Neural Net, the observation to use is:
        [
            [Binary current attacker slice],
            [Binary attackers slice],
            [Binary defenders slice],
            [Binary walls slice],
        ]
        """
        return np.stack((self.attackers_array, self.defenders_array, self.walls_array))

    def defenders_pov(self) -> np.array:
        """
        For the defenders Neural Net, the observation to use is:
        [
            [Binary defenders slice],
            [Binary attackers slice],
            [Binary walls slice],
        ]
        """
        return np.stack((self.defenders_array, self.attackers_array, self.walls_array))

    def nn_attackers_pov(self, attacker_position) -> np.array:
        """
        For the attackers Neural Net, the observation to use is:
        [
            [Binary current attacker slice],
            [Binary attackers slice],
            [Binary defenders slice],
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
                self.defenders_array,
                self.walls_array,
            )
        )

    def nn_defenders_pov(self, defender_position) -> np.array:
        """
        For the defenders Neural Net, the observation to use is:
        [
            [Binary current defender slice],
            [Binary defenders slice],
            [Binary attackers slice],
            [Binary walls slice],
        ]
        """
        current_defender_slice = np.zeros(
            shape=(self.map_size[0], self.map_size[1]), dtype=np.float32
        )
        current_defender_slice[defender_position[0]][defender_position[1]] = 1.0
        return np.stack(
            (
                current_defender_slice,
                self.defenders_array,
                self.attackers_array,
                self.walls_array,
            )
        )

    def update_observation(
        self,
        attackers_position,
        defenders_position,
        walls_position,
        new_attackers_position,
        new_defenders_position,
        new_walls_position,
    ):
        """
        Update the positions of the attackers, defenders and walls with new positions.
        """
        # Update attackers array
        self.attackers_array[attackers_position[:, 0], attackers_position[:, 1]] = 0.0
        self.attackers_array[
            new_attackers_position[:, 0], new_attackers_position[:, 1]
        ] = 1.0
        # Update defenders array
        if np.any(defenders_position):
            self.defenders_array[
                defenders_position[:, 0], defenders_position[:, 1]
            ] = 0.0
        if np.any(new_defenders_position):
            self.defenders_array[
                new_defenders_position[:, 0], new_defenders_position[:, 1]
            ] = 1.0
        # Update walls array
        if np.any(walls_position):
            self.walls_array[walls_position[:, 0], walls_position[:, 1]] = 0.0
        if np.any(new_walls_position):
            self.walls_array[new_walls_position[:, 0], new_walls_position[:, 1]] = 1.0


def init_binary_map(map_size, attackers, defenders) -> list:
    """
    This method initializes a binary map of a DAv environment.
    Args:
        map_size (tuple): size of the input map. Ex: (20,20).
        attackers (list): List of the attackers of the map. Ex: [Attacker1, Attacker2]
        defenders (list): List of the defenders of the map. Ex: [Defenders1, Defenders2]

    Output:
        BinaryMapObservation: A binary map representation of the input:
            - Slice x: array of size map_size with 0 every where and 1 at the position of the attackers
            - Slice y: array of size map_size with 0 every where and 1 at the position of the defenders
            - Slice z: array of size map_size with 0 every where and 1 at the position of the walls
    """
    walls_tensor = np.zeros(
        shape=(map_size[0], map_size[1]), dtype=np.float32
    )  # At the initialisation, there is no wall.

    # Initialisation of the attackers position
    attackers_tensor = np.zeros(shape=(map_size[0], map_size[1]), dtype=np.float32)
    for attacker in attackers:
        attackers_tensor[attacker.get_position()[0]][attacker.get_position()[1]] = 1.0

    # Initialisation of the defenders position
    defenders_tensor = np.zeros(shape=(map_size[0], map_size[1]), dtype=np.float32)
    for defender in defenders:
        defenders_tensor[defender.get_position()[0]][defender.get_position()[1]] = 1.0

    return BinaryMapObservation(
        attackers_tensor, defenders_tensor, walls_tensor, map_size
    )
