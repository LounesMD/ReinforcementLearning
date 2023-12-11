import torch

class DQN:
    """
    An implementation of DQN using CNN. The DQN implementation works as follow:
    [States] ->
    [Conv2d -> ReLU -> ... -> Conv2d -> ReLU] ->
    [Flatten] ->
    [Linear -> ReLU -> ... -> Linear -> ReLU] ->
    [Output]
    """

    def __init__(
        self,
        map_size: tuple,
        history_length: int = 4,
        nb_layers: int = 2,
        nb_filters: list = [16, 32],
        kernel_size: list = [8, 4],
        stride: list = [2, 2],
        padding: list = [1, 1],
        last_mlp_size: int = 256,
        output_size: int = 5,
        mlp_size: list = [256],
    ) -> None:
        assert history_length > 0
        self.history_length = history_length
        self.nb_layers = nb_layers
        self.map_size = map_size
        self.nb_filters = nb_filters
        self.kernel_size = kernel_size
        self.last_mlp_size = last_mlp_size
        self.output_size = output_size
        self.stride = stride
        self.padding = padding
        self.mlp_size = mlp_size
        self.conv_model = self._init_conv_model()
        self.mlp_model = self._init_mlp_model()

    def _init_conv_model(self):
        """
        Conv part of the Neural network. This part is composed of the following elements:
        Conv2d -> ReLU -> ... -> Conv2d -> ReLU
        """
        modules = list()
        prev_in_channels = self.history_length
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

    def _init_mlp_model(self):
        """
        Mlp part of the Neural network. This part is composed of the following elements:
        Linear -> ReLU -> ... -> Linear -> ReLU
        """
        modules = list()
        prev_size = self.nb_filters[-1] * (self.kernel_size[-1] ** 2) # The number of neurons for the first layer is: Number of filters * kernel_size_w * kernel_size_h
        for _, size in enumerate(self.mlp_size):
            modules.append(torch.nn.Linear(prev_size, size))
            modules.append(torch.nn.ReLU())
            prev_size = size
        modules.append(torch.nn.Linear(prev_size, self.output_size))
        return torch.nn.Sequential(*modules)

    def forward(self, input):
        output_conv = self.conv_model(input)
        input_mlp = torch.flatten(output_conv)
        output = self.mlp_model(input_mlp)
        return output

    def update(self):
        pass

    def loss(self, input, target):
        pass
