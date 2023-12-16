import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np

import Codes
from Codes.rl_agents.agents.DQN.DQN import DQN_agent


def average_of_elements(list_of_lists):
    max_length = max(len(lst) for lst in list_of_lists)
    averages = []
    for i in range(max_length):
        sum_elements = 0
        count = 0
        for lst in list_of_lists:
            if i < len(lst):
                sum_elements += lst[i]
                count += 1
        if count > 0:
            averages.append(sum_elements / count)
    return averages


def main():
    render = False
    env = gym.make(
        "env_DAv-v0",
        rendering=render,
        map_size=(10, 10),
        number_of_defensers=1,
        number_of_attackers=1,
        step_limit=250,
    )
    map_size = env.map_size
    dqn_attackers = DQN_agent(input_size=(4, map_size[0], map_size[1]), action_space=4)
    dqn_defensers = DQN_agent(input_size=(4, map_size[0], map_size[1]), action_space=5)
    def_scores_list = list()
    episode_length_list = list()
    attackers_loss = list()
    defensers_loss = list()
    def_alive = list()
    n_games = 2
    for idx in range(n_games):
        att_loss = list()
        def_loss = list()
        att_scores = 0
        def_scores = 0
        episode_length = 0
        env.reset()
        while not env.terminated and not env.truncated:
            episode_length += 1
            actions = list()
            defensers_action = list()
            attackers_action = list()
            defensers_state = list()
            attackers_state = list()

            # We compute the actions for the attackers and defensers
            for attacker in env.attackers:
                state = env.binary_map.nn_attackers_pov(attacker.get_position())
                state = state[np.newaxis,]
                action = dqn_attackers.get_action(state)
                attackers_state.append(state)
                actions.append(action)
                attackers_action.append(action)

            for defenser in env.defensers:
                if defenser.is_alive():
                    state = env.binary_map.nn_defensers_pov(defenser.get_position())
                    state = state[np.newaxis,]
                    action = dqn_defensers.get_action(state)
                    defensers_state.append(state)
                    actions.append(action)
                    defensers_action.append(action)

            # We apply the actions to our environment
            obs, rewards, terminated, _, _ = env.step(actions)
            att_scores += sum(rewards[0])
            def_scores += sum(rewards[1])

            # We store the transitions for the defensers and attackers
            for i, attacker in enumerate(env.attackers):
                dqn_attackers.store_transition(
                    attackers_state[i],
                    attackers_action[i],
                    rewards[0][i],
                    obs.nn_attackers_pov(attacker.get_position()),
                    terminated,
                )

            for i, defenser in enumerate(
                [deff for deff in env.defensers if deff.is_alive()]
            ):
                dqn_defensers.store_transition(
                    defensers_state[i],
                    defensers_action[i],
                    rewards[1][i],
                    obs.nn_defensers_pov(defenser.get_position()),
                    terminated,
                )

            # Learning phase
            res = dqn_attackers.learn()
            if res != None:
                att_loss.append(res.cpu().detach().numpy())
            res = dqn_defensers.learn()
            if res != None:
                def_loss.append(res.cpu().detach().numpy())

            if render:
                env.render()

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
        defensers_loss.append(def_loss)
        attackers_loss.append(att_loss)

    p1 = average_of_elements(defensers_loss)
    p2 = average_of_elements(attackers_loss)
    plt.plot([i for i in range(len(p2))], p2, label="loss attackers")
    plt.legend()
    plt.show()
    plt.plot([i for i in range(len(p1))], p1, label="loss defensers")
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
