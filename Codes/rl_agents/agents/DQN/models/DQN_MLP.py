import torch

from Codes.rl_agents.agents.DQN.models.DQN_model import DQN_Model
from Codes.rl_agents.agents.utils import conv2d_output_size


class DQN_MLP(DQN_Model):
    """
    A version of DQN using only linear layers.
    The input states are of size (h_image, w_image, nb_channels)
    """

    def __init__(
        self,
        input_size: tuple,
        history_size: int = 1,
        output_size: int = 5,
        learning_rate: float = 0.001,
        critertion: torch.nn = torch.nn.MSELoss,
        optimizer: torch.optim = torch.optim.AdamW,
        device: str = "mps",  # Use mps for mac.
    ) -> None:
        super().__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.learning_rate = learning_rate
        self.critertion = critertion()
        self.model = self._init_model()

        self.optimizer = optimizer(
            params=self.parameters(), lr=self.learning_rate, amsgrad=True
        )
        self.device = torch.device(device)

    def _init_model(self):
        return

    def forward(self, input):
        return self.model(input)
