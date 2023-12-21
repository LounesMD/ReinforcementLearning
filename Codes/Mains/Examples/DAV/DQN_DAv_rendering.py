import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np

import Codes
from Codes.Mains.Examples.DAv.utils.binary_observation_utils import init_binary_map
from Codes.rl_agents.agents.DQN.DQN import DQN_agent


def main():
    """
    This main loads existing policies and use them to plot the agents behavior.
    """
    render = True
    env = gym.make(
        "env_DAv-v0",
        rendering=render,
        map_size=(15, 15),
        number_of_defenders=1,
        number_of_attackers=1,
        step_limit=30,
    )
    total_step = 0
    map_size = env.unwrapped.map_size
    attacker_action_space = 4
    defender_action_space = 5
    dqn_attackers = DQN_agent(
        input_size=(4, map_size[0], map_size[1]), action_space=attacker_action_space
    )
    dqn_defenders = DQN_agent(
        input_size=(4, map_size[0], map_size[1]), action_space=defender_action_space
    )

    dqn_attackers.epsilon = 0.0
    dqn_attackers.load_weights("dqn_attackers_weights_iteration_59750.pth")
    dqn_defenders.epsilon = 0.0
    dqn_defenders.load_weights("dqn_defenders_weights_iteration_59750.pth")

    n_games = 1
    for idx in range(n_games):
        episode_length = 0
        env.reset()
        input_for_CNN = init_binary_map(
            map_size=map_size,
            attackers=env.unwrapped.attackers,
            defenders=env.unwrapped.defenders,
        )
        while not env.unwrapped.terminated and not env.unwrapped.truncated:
            episode_length += 1
            actions = list()
            defenders_action = list()
            attackers_action = list()
            defenders_state = list()
            attackers_state = list()

            current_attackers_position = list()
            # We compute the actions for the attackers and defenders
            for attacker in env.unwrapped.attackers:
                position = attacker.get_position()
                current_attackers_position.append(attacker.get_position())
                state = input_for_CNN.nn_attackers_pov(attacker.get_position())
                state = state[np.newaxis,]
                action = dqn_attackers.get_action(state)
                attackers_state.append(state)
                actions.append(action)
                attackers_action.append(action)

            current_defenders_position = list()
            for defender in env.unwrapped.defenders:
                if defender.is_alive():
                    position = defender.get_position()
                    current_defenders_position.append(defender.get_position())
                    state = input_for_CNN.nn_defenders_pov(defender.get_position())
                    state = state[np.newaxis,]
                    action = dqn_defenders.get_action(state)
                    defenders_state.append(state)
                    actions.append(action)
                    defenders_action.append(action)

            current_walls_position = [
                wall.get_position()
                for wall in env.unwrapped.walls
                if (not wall.is_broken())
            ]
            # We apply the actions to our environment
            assert len(actions) == len(env.unwrapped.attackers) + len(
                [deff for deff in env.unwrapped.defenders if deff.is_alive()]
            )
            obs, _, _, _, _ = env.step(actions)
            input_for_CNN.update_observation(
                attackers_position=np.array(current_attackers_position),
                defenders_position=np.array(current_defenders_position),
                walls_position=np.array(current_walls_position),
                new_attackers_position=obs["attackers_position"],
                new_defenders_position=obs["defenders_position"],
                new_walls_position=obs["walls_position"],
            )

            if render:
                env.render()

            total_step += 1


if __name__ == "__main__":
    main()
