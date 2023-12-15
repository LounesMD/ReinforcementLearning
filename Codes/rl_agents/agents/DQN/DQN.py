import numpy as np
import torch

from Codes.rl_agents.agents.DQN.models.DQN_CNN import DQN_CNN
from Codes.rl_agents.agents.DQN.models.DQN_model import DQN_Model


class DQN_agent:
    """
    A generic class for different versions of DQN.
    """

    def __init__(
        self,
        input_size: tuple,
        history_size: int = 1,
        nb_mlp_layers: int = 2,
        nb_cnn_layers: int = 2,
        nb_filters: list = [16, 32],
        kernel_size: list = [8, 4],
        stride: list = [2, 2],
        padding: list = [1, 1],
        last_mlp_size: int = 256,
        action_space: int = 5,
        output_size: int = 5,
        learning_rate: float = 0.001,
        model: DQN_Model = DQN_CNN,
        mlp_size: list = [256],
        gamma: float = 0.95,
        mem_size: int = 10000,
        batch_size: int = 64,
        epsilon: float = 1,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 5e-4,
        optimizer: torch.optim = torch.optim.AdamW,
    ) -> None:
        self.nb_mlp_layers = nb_mlp_layers
        self.nb_cnn_layers = nb_cnn_layers
        self.input_size = input_size
        self.nb_filters = nb_filters
        self.kernel_size = kernel_size
        self.last_mlp_size = last_mlp_size
        self.output_size = output_size
        self.stride = stride
        self.padding = padding
        self.mlp_size = mlp_size
        self.action_space = action_space
        self.learning_rate = learning_rate

        self.batch_size = batch_size
        # In this version we use only one model instead of two.
        self.model = model(
            input_size=self.input_size,
            nb_cnn_layers=self.nb_cnn_layers,
            nb_mlp_layers=self.nb_mlp_layers,
            kernel_size=self.kernel_size,
            stride=self.stride,
            padding=self.padding,
            last_mlp_size=self.last_mlp_size,
            action_space=self.action_space,
            output_size=self.output_size,
            mlp_size=self.mlp_size,
            learning_rate=self.learning_rate,
        )
        self.model.to(self.model.device)

        self.optimizer = optimizer(
            params=self.model.parameters(), lr=self.learning_rate, amsgrad=True
        )

        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.gamma = gamma

        # Memory vectors to store observations
        self.mem_size = mem_size
        self.mem_use = 0
        self.mem_state = np.zeros(
            shape=(self.mem_size, *self.input_size), dtype=np.float32
        )
        self.mem_action = np.zeros(shape=(self.mem_size,), dtype=np.int32)
        self.mem_reward = np.zeros(shape=(self.mem_size,), dtype=np.float32)
        self.mem_done = np.zeros(shape=(self.mem_size,), dtype=bool)
        self.mem_next_state = np.zeros(
            shape=(self.mem_size, *self.input_size), dtype=np.float32
        )

    def espilon_greedy(self, epsilon, actions, action_space):
        """
        TODO: refactor this method to a class.
        """
        if np.random.random() > epsilon:
            action = torch.argmax(actions).item()
        else:
            action = np.random.choice(action_space)
        return action

    def store_transition(self, state, action, reward, next_state, done):
        """
        Store a transition in the local memory buffer.
        Args:
            state (np.ndarray): representation of the current state
            action (int): action perform in the state
            reward (float): reward from step(state,action)
            next_state (np.ndarray): state after step(state, action)
            done (bool): True if state is a terminal state, Fasle otherwise
        """
        index = self.mem_use % self.mem_size
        self.mem_state[index] = state
        self.mem_action[index] = action
        self.mem_reward[index] = reward
        self.mem_done[index] = done
        self.mem_next_state[index] = next_state

        self.mem_use += 1

    def get_action(self, observation):
        state = torch.tensor(observation).to(self.model.device)
        actions = self.model.forward(state)
        action = self.espilon_greedy(self.epsilon, actions, self.action_space)
        return action

    def learn(self):
        if self.mem_use < self.batch_size:
            return

        self.model.optimizer.zero_grad()

        # Pick a random learning element from the memory
        index = min(self.mem_use, self.mem_size)
        learning_index = np.random.choice(index, self.batch_size, replace=False)
        batch_index = np.arange(self.batch_size, dtype=np.int32)

        state_batch = torch.tensor(self.mem_state[learning_index]).to(self.model.device)
        action_batch = torch.tensor(self.mem_action[learning_index])
        reward_batch = torch.tensor(self.mem_reward[learning_index]).to(
            self.model.device
        )
        done_batch = torch.tensor(self.mem_done[learning_index]).to(self.model.device)
        next_state_batch = torch.tensor(self.mem_next_state[learning_index]).to(
            self.model.device
        )

        q_state_action = self.model(state_batch)[batch_index, action_batch]

        q_next_state_action = self.model.forward(next_state_batch)
        q_next_state_action[done_batch] = 0.0
        q_next_state_action = torch.max(q_next_state_action, dim=1)[0]

        target_q_value = (
            reward_batch + self.gamma * q_next_state_action
        )  # TODO: should not we do input_batch.reward + self.gamma * (best_next_values - q_state_action)?

        loss = self.model.critertion(q_state_action, target_q_value)

        loss.backward()
        self.model.optimizer.step()
        self.epsilon = (
            self.epsilon - self.epsilon_decay
            if self.epsilon > self.epsilon_min
            else self.epsilon_min
        )
        return loss
