import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np

import Codes
from Codes.Mains.Examples.utils.binary_observation_utils import init_binary_map
from Codes.rl_agents.agents.DQN.DQN import DQN_agent


def main():
    render = False
    env = gym.make(
        "env_DAv-v0",
        rendering=render,
        map_size=(15, 15),
        number_of_defensers=1,
        number_of_attackers=1,
        step_limit=200,
    )
    total_step = 0
    map_size = env.map_size
    attacker_action_space = 4
    defenser_action_space = 5
    dqn_attackers = DQN_agent(
        input_size=(4, map_size[0], map_size[1]),
        action_space=attacker_action_space,
        learning_rate=0.001,
    )
    dqn_defensers = DQN_agent(
        input_size=(4, map_size[0], map_size[1]),
        action_space=defenser_action_space,
        learning_rate=0.0005,
    )
    def_scores_list = list()
    episode_length_list = list()
    def_alive = list()
    att_loss = list()
    def_loss = list()

    n_games = 10000
    for idx in range(n_games):
        att_scores = 0
        def_scores = 0
        episode_length = 0
        env.reset()
        input_for_CNN = init_binary_map(
            map_size=map_size, attackers=env.attackers, defensers=env.defensers
        )
        while not env.terminated and not env.truncated:
            episode_length += 1
            actions = list()
            defensers_action = list()
            attackers_action = list()
            defensers_state = list()
            attackers_state = list()

            current_attackers_position = list()
            # We compute the actions for the attackers and defensers
            for attacker in env.attackers:
                current_attackers_position.append(attacker.get_position())
                state = input_for_CNN.nn_attackers_pov(attacker.get_position())
                state = state[np.newaxis,]
                action = dqn_attackers.get_action(state)
                attackers_state.append(state)
                actions.append(action)
                attackers_action.append(action)

            current_defensers_position = list()
            for defenser in env.defensers:
                if defenser.is_alive():
                    current_defensers_position.append(defenser.get_position())
                    state = input_for_CNN.nn_defensers_pov(defenser.get_position())
                    state = state[np.newaxis,]
                    action = dqn_defensers.get_action(state)
                    defensers_state.append(state)
                    actions.append(action)
                    defensers_action.append(action)

            current_walls_position = [
                wall.get_position() for wall in env.walls if (not wall.is_broken())
            ]
            # We apply the actions to our environment
            assert len(actions) == len(env.attackers) + len(
                [deff for deff in env.defensers if deff.is_alive()]
            )
            obs, rewards, terminated, truncated, _ = env.step(actions)
            att_scores += sum(rewards[0])
            def_scores += sum(rewards[1])
            input_for_CNN.update_observation(
                attackers_position=np.array(current_attackers_position),
                defensers_position=np.array(current_defensers_position),
                walls_position=np.array(current_walls_position),
                new_attackers_position=obs["attackers_position"],
                new_defensers_position=obs["defensers_position"],
                new_walls_position=obs["walls_position"],
            )

            # We store the transitions for the defensers and attackers
            for i, attacker in enumerate(env.attackers):
                dqn_attackers.store_transition(
                    attackers_state[i],
                    attackers_action[i],
                    rewards[0][i],
                    input_for_CNN.nn_attackers_pov(attacker.get_position()),
                    terminated and truncated,
                )

            for i, defenser in enumerate(
                [deff for deff in env.defensers if deff.is_alive()]
            ):
                dqn_defensers.store_transition(
                    defensers_state[i],
                    defensers_action[i],
                    rewards[1][i],
                    input_for_CNN.nn_defensers_pov(defenser.get_position()),
                    terminated and truncated,
                )

            # For the dead defensers, we suppose they are in an absorbing state where they are stuck and the reward is 0.
            for i, defenser in enumerate(
                [deff for deff in env.defensers if (not deff.is_alive())]
            ):
                state = input_for_CNN.defensers_pov()
                state = np.concatenate(
                    (np.zeros(shape=(1, map_size[0], map_size[1])), state), axis=0
                )
                state = state[np.newaxis,]
                dqn_defensers.store_transition(
                    state,
                    np.random.choice(
                        defenser_action_space
                    ),  # We pick a random action as the agent is in an absorbing state
                    -1,  # A zero reward when they are dead
                    state,  # Stuck to the same state
                    True,
                )

            # Learning phase
            res = dqn_attackers.learn()
            if res != None:
                att_loss.append(res.cpu().detach().numpy())
            res = dqn_defensers.learn()
            if res != None:
                def_loss.append(res.cpu().detach().numpy())

            if total_step % dqn_attackers.update_rate == 0:
                dqn_attackers.update_model()
            if total_step % dqn_defensers.update_rate == 0:
                dqn_defensers.update_model()

            if idx % 250 == 0:
                dqn_attackers.save_weights(
                    "dqn_attackers_weights_iteration_" + str(idx) + ".pth"
                )
                dqn_defensers.save_weights(
                    "dqn_defensers_weights_iteration_" + str(idx) + ".pth"
                )

            total_step += 1

        print("Episode: " + str(idx) + ", " + str(episode_length) + " steps.")
        print(
            "Rewards are: "
            + str(att_scores)
            + " for the attackers and: "
            + str(def_scores)
            + " for the defensers."
        )
        print(
            "Defensers alive: "
            + str(len([deff for deff in env.defensers if deff.is_alive()]))
        )
        def_alive.append(len([deff for deff in env.defensers if deff.is_alive()]))
        def_scores_list.append(def_scores)
        episode_length_list.append(episode_length)

    plt.plot([i for i in range(len(def_loss))], def_loss, label="loss attackers")
    plt.legend()
    plt.show()
    plt.plot([i for i in range(len(att_loss))], att_loss, label="loss defensers")
    plt.legend()
    plt.show()
    plt.plot(
        [i for i in range(len(def_scores_list))],
        def_scores_list,
        label="defensers score",
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
        label="number of defensers alive",
    )
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
