import torch


class ObservationType(object):
    def __init__(self) -> None:
        pass


class BinaryMapObservation(ObservationType):
    def __init__(
        self,
        attackers_tensor: torch.Tensor,
        defensers_tensor: torch.Tensor,
        walls_tensor: torch.Tensor,
    ) -> None:
        super().__init__()
        self.attackers_tensor = attackers_tensor
        self.defensers_tensor = defensers_tensor
        self.walls_tensor = walls_tensor

    def get_attackers_tensor(self) -> torch.Tensor:
        return self.attackers_tensor

    def update_attackers_tensor(self, position, element) -> None:
        self.attackers_tensor[position[0]][position[1]] = element

    def get_defensers_tensor(self) -> torch.Tensor:
        return self.defensers_tensor

    def update_defensers_tensor(self, position, element) -> None:
        self.defensers_tensor[position[0]][position[1]] = element

    def get_walls_tensor(self) -> torch.Tensor:
        return self.walls_tensor

    def update_walls_tensor(self, position, element) -> None:
        self.walls_tensor[position[0]][position[1]] = element

    def observe_attackers_pov(self) -> torch.Tensor:
        """
        For the attackers Neural Net, the observation to use is:
        [
            [Binary attackers slice],
            [Binary defensers slice],
            [Binary walls slice],
        ]
        """
        return torch.stack(
            (self.attackers_tensor, self.defensers_tensor, self.walls_tensor)
        )

    def observe_defensers_pov(self) -> torch.Tensor:
        """
        For the defensers Neural Net, the observation to use is:
        [
            [Binary defensers slice],
            [Binary attackers slice],
            [Binary walls slice],
        ]
        """
        return torch.stack(
            (self.defensers_tensor, self.attackers_tensor, self.walls_tensor)
        )
