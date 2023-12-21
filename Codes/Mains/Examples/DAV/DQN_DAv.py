import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np

import Codes
from Codes.Mains.Examples.DAv.utils.binary_observation_utils import init_binary_map
from Codes.rl_agents.agents.DQN.DQN import DQN_agent


def main():
    """
    This main trains agents with DAv environment.
    """
    render = False
    env = gym.make(
        "env_DAv-v0",
        rendering=render,
        map_size=(15, 15),
        number_of_defenders=1,
        number_of_attackers=1,
        step_limit=200,
    )
    total_step = 0
    map_size = env.unwrapped.map_size
    attacker_action_space = 4
    defender_action_space = 5
    dqn_attackers = DQN_agent(
        input_size=(4, map_size[0], map_size[1]),
        action_space=attacker_action_space,
        learning_rate=0.001,
        epsilon_min=0.1,
    )
    dqn_defenders = DQN_agent(
        input_size=(4, map_size[0], map_size[1]),
        action_space=defender_action_space,
        learning_rate=0.0005,
    )
    def_scores_list = list()
    episode_length_list = list()
    def_alive = list()
    att_loss = list()
    def_loss = list()

    n_games = 60000
    for idx in range(n_games):
        att_scores = 0
        def_scores = 0
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
            obs, rewards, terminated, truncated, _ = env.step(actions)
            att_scores += sum(rewards[0])
            def_scores += sum(rewards[1])
            input_for_CNN.update_observation(
                attackers_position=np.array(current_attackers_position),
                defenders_position=np.array(current_defenders_position),
                walls_position=np.array(current_walls_position),
                new_attackers_position=obs["attackers_position"],
                new_defenders_position=obs["defenders_position"],
                new_walls_position=obs["walls_position"],
            )

            # We store the transitions for the defenders and attackers
            for i, attacker in enumerate(env.unwrapped.attackers):
                dqn_attackers.store_transition(
                    attackers_state[i],
                    attackers_action[i],
                    rewards[0][i],
                    input_for_CNN.nn_attackers_pov(attacker.get_position()),
                    terminated and truncated,
                )

            for i, defender in enumerate(
                [deff for deff in env.unwrapped.defenders if deff.is_alive()]
            ):
                dqn_defenders.store_transition(
                    defenders_state[i],
                    defenders_action[i],
                    rewards[1][i],
                    input_for_CNN.nn_defenders_pov(defender.get_position()),
                    terminated and truncated,
                )

            # For the dead defenders, we suppose they are in an absorbing state where they are stuck and the reward is 0.
            for i, defender in enumerate(
                [deff for deff in env.unwrapped.defenders if (not deff.is_alive())]
            ):
                state = input_for_CNN.defenders_pov()
                state = np.concatenate(
                    (np.zeros(shape=(1, map_size[0], map_size[1])), state), axis=0
                )
                state = state[np.newaxis,]
                dqn_defenders.store_transition(
                    state,
                    np.random.choice(
                        defender_action_space
                    ),  # We pick a random action as the agent is in an absorbing state
                    -1,  # A zero reward when they are dead
                    state,  # Stuck to the same state
                    True,
                )

            # Learning phase
            res = dqn_attackers.learn()
            if res != None:
                att_loss.append(res.cpu().detach().numpy())
            res = dqn_defenders.learn()
            if res != None:
                def_loss.append(res.cpu().detach().numpy())

            if total_step % dqn_attackers.update_rate == 0:
                dqn_attackers.update_model()
            if total_step % dqn_defenders.update_rate == 0:
                dqn_defenders.update_model()

            if idx % 250 == 0:
                dqn_attackers.save_weights(
                    "dqn_attackers_weights_iteration_" + str(idx) + ".pth"
                )
                dqn_defenders.save_weights(
                    "dqn_defenders_weights_iteration_" + str(idx) + ".pth"
                )

            total_step += 1

        print("Episode: " + str(idx) + ", " + str(episode_length) + " steps.")
        print(
            "Rewards are: "
            + str(att_scores)
            + " for the attackers and: "
            + str(def_scores)
            + " for the defenders."
        )
        print(
            "Defenders alive: "
            + str(len([deff for deff in env.unwrapped.defenders if deff.is_alive()]))
        )
        def_alive.append(
            len([deff for deff in env.unwrapped.defenders if deff.is_alive()])
        )
        def_scores_list.append(def_scores)
        episode_length_list.append(episode_length)

    plt.plot([i for i in range(len(def_loss))], def_loss, label="loss attackers")
    plt.legend()
    plt.show()
    plt.plot([i for i in range(len(att_loss))], att_loss, label="loss defenders")
    plt.legend()
    plt.show()
    plt.plot(
        [i for i in range(len(def_scores_list))],
        def_scores_list,
        label="defenders score",
    )
    plt.plot(
        [i for i in range(len(episode_length_list))],
        episode_length_list,
        label="episode_length",
    )
    plt.legend()
    plt.show()
    plt.plot(
        [i for i in range(len(def_alive))],
        def_alive,
        label="number of defenders alive",
    )
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
