from Codes.rl_agents.agents.DQN.models.DQN_model import DQN_Model
import torch


class DQN_CNN(DQN_Model):
    def __init__(
        self,
        history_size: int = 1,
        in_channels: int = 3,
        nb_layers: int = 2,
        nb_filters: list = [16, 32],
        kernel_size: list = [8, 4],
        stride: list = [2, 2],
        padding: list = [1, 1],
        last_mlp_size: int = 256,
        action_space: int = 4,
        output_size: int = 5,
        mlp_size: list = [256],
        learning_rate: float = 0.003,
        critertion: torch.nn = torch.nn.MSELoss,
        optimizer: torch.optim = torch.optim.AdamW,
    ) -> None:
        super().__init__()
        assert in_channels > 0
        self.in_channels = in_channels
        self.nb_layers = nb_layers
        self.nb_filters = nb_filters
        self.kernel_size = kernel_size
        self.last_mlp_size = last_mlp_size
        self.output_size = output_size
        self.stride = stride
        self.padding = padding
        self.mlp_size = mlp_size
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.critertion = critertion
        # self.model = self._init_one_model()
        self.cnn_layers = self._init_conv_layers()
        self.linear_layers = self._init_linear_layers()

        self.optimizer = optimizer(
            params=self.parameters(), lr=self.learning_rate, amsgrad=True
        )

    def _init_conv_layers(self):
        modules = list()
        prev_in_channels = self.in_channels
        for i in range(self.nb_layers):
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
        prev_size = self.nb_filters[-1] * (
            self.kernel_size[-1] ** 2
        )  # The number of neurons for the first layer is: Number of filters * kernel_size_w * kernel_size_h
        for _, size in enumerate(self.mlp_size):
            modules.append(torch.nn.Linear(prev_size, size))
            modules.append(torch.nn.ReLU())
            prev_size = size
        modules.append(torch.nn.Linear(prev_size, self.output_size))
        return torch.nn.Sequential(*modules)

    def _init_one_model(self):
        modules = list()
        prev_in_channels = self.in_channels
        for i in range(self.nb_layers):
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

        prev_size = self.nb_filters[-1] * (
            self.kernel_size[-1] ** 2
        )  # The number of neurons for the first layer is: Number of filters * kernel_size_w * kernel_size_h
        for _, size in enumerate(self.mlp_size):
            modules.append(torch.nn.Linear(prev_size, size))
            modules.append(torch.nn.ReLU())
            prev_size = size
        modules.append(torch.nn.Linear(prev_size, self.output_size))
        return torch.nn.Sequential(*modules)

    def forward(self, input):
        cnn_output = self.cnn_layers(input)
        linear_input = torch.flatten(cnn_output)
        output = self.linear_layers(linear_input)
        return output
