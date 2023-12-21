import torch

from Codes.rl_agents.agents.DQN.models.DQN_model import DQN_Model
from Codes.rl_agents.agents.utils import conv2d_output_size


class DQN_CNN(DQN_Model):
    """
    A version of DQN using conv and linear layers as presented by D. Silver in: https://www.davidsilver.uk/wp-content/uploads/2020/03/deep_rl_tutorial_small_compressed.pdf

    [States] ->
    [Conv2d -> ReLU -> ... -> Conv2d -> ReLU] ->
    [Flatten] ->
    [Linear -> ReLU -> ... -> Linear -> ReLU] ->
    [Output].

    The input states are of size (h_image, w_image, nb_channels)
    """

    def __init__(
        self,
        input_size: tuple,
        history_size: int = 1,
        nb_cnn_layers: int = 2,
        nb_mlp_layers: int = 2,
        nb_filters: list = [16, 32],
        kernel_size: list = [8, 4],
        stride: list = [1, 1],
        padding: list = [1, 1],
        output_size: int = 5,
        mlp_size: list = [256],
        learning_rate: float = 0.001,
        critertion: torch.nn = torch.nn.MSELoss,
        optimizer: torch.optim = torch.optim.AdamW,
        device: str = "mps",  # Use mps for mac.
    ) -> None:
        super().__init__()
        self.input_size = input_size
        self.nb_cnn_layers = nb_cnn_layers
        self.nb_mlp_layers = nb_mlp_layers
        self.nb_filters = nb_filters
        self.kernel_size = kernel_size
        self.output_size = output_size
        self.stride = stride
        self.padding = padding
        self.mlp_size = mlp_size
        self.learning_rate = learning_rate
        self.critertion = critertion()
        self.cnn_layers = self._init_conv_layers()
        self.linear_layers = self._init_linear_layers()

        self.optimizer = optimizer(
            params=self.parameters(), lr=self.learning_rate, amsgrad=True
        )
        self.device = torch.device(device)

    def _init_conv_layers(self):
        modules = list()
        prev_in_channels = self.input_size[0]
        for i in range(self.nb_cnn_layers):
            modules.append(
                torch.nn.Conv2d(
                    in_channels=prev_in_channels,
                    out_channels=self.nb_filters[i],
                    kernel_size=self.kernel_size[i],
                    stride=self.stride[i],
                    padding=self.padding[i],
                )
            )
            modules.append(torch.nn.ReLU())
            prev_in_channels = self.nb_filters[i]
        return torch.nn.Sequential(*modules)

    def _init_linear_layers(self):
        modules = []
        input_size = self.input_size
        for i in range(self.nb_cnn_layers):
            input_size = conv2d_output_size(
                input_size,
                self.nb_filters[i],
                self.padding[i],
                self.kernel_size[i],
                self.stride[i],
            )
        prev_size = input_size[0] * input_size[1] * input_size[2]
        for _, size in enumerate(self.mlp_size):
            modules.append(torch.nn.Linear(prev_size, size))
            modules.append(torch.nn.ReLU())
            prev_size = size
        modules.append(torch.nn.Linear(prev_size, self.output_size))
        return torch.nn.Sequential(*modules)

    def forward(self, input):
        cnn_output = self.cnn_layers(input)
        linear_input = cnn_output.view(cnn_output.shape[0], -1)
        output = self.linear_layers(linear_input)
        return output
