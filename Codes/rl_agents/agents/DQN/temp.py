from Codes.rl_agents.agents.DQN.DQN import DQN_agent
from Codes.rl_agents.agents.DQN.temp2 import Net
import numpy as np


map_size = (20, 20)
dqn = DQN_agent(map_size=map_size, state_dim=(3, map_size[0], map_size[1]))
import torch

test_input = np.stack(
    (
        np.zeros(shape=map_size, dtype=np.float32),
        np.zeros(shape=map_size, dtype=np.float32),
        np.zeros(shape=map_size, dtype=np.float32),
    )
)
res = dqn.model.cnn_layers(torch.tensor(test_input))
t2 = np.stack((test_input, test_input))
import pdb

pdb.set_trace()
