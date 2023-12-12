from Codes.rl_agents.agents.utils import Batch_mode
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
        learning_rate: float = 0.0001,
        gamma: float = 0.9,
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
        self.value_model = self._init_model
        self.target_model = self._init_model

        self.learning_rate = learning_rate
        self.gamma = gamma
        self.critertion = torch.nn.SmoothL1Loss()
        self.optimizer = torch.optim.AdamW(
            params=self.value_model, lr=self.learning_rate, amsgrad=True
        )

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
        prev_size = self.nb_filters[-1] * (
            self.kernel_size[-1] ** 2
        )  # The number of neurons for the first layer is: Number of filters * kernel_size_w * kernel_size_h
        for _, size in enumerate(self.mlp_size):
            modules.append(torch.nn.Linear(prev_size, size))
            modules.append(torch.nn.ReLU())
            prev_size = size
        modules.append(torch.nn.Linear(prev_size, self.output_size))
        return torch.nn.Sequential(*modules)

    def _init_model(self, input):
        output_conv = self.conv_model(input)
        input_mlp = torch.flatten(output_conv)
        output = self.mlp_model(input_mlp)
        return output

    def loss(self, input_batch: Batch_mode):
        q_state_action = self.value_model(
            input_batch.state
        )  # We predict Q(s_t,.) for all given states
        q_state_action = q_state_action.gather(
            1, input_batch.action.unsqueeze(1)
        )  # We keep only Q(s_t,a_t)

        best_next_values = self.target_model(input_batch.next_state).max(1)
        target_q_values = (
            input_batch.reward + self.gamma * best_next_values
        )  # TODO: should not we do input_batch.reward + self.gamma * (best_next_values - q_state_action)?

        loss = self.critertion(q_state_action, target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
