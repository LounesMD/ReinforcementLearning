import gymnasium as gym

import Codes


def main():
    env = gym.make("env_cartPole-v0")
    env.reset()
    while not env.unwrapped.terminated and not env.unwrapped.truncated:
        actions = 0  # Put your actions vector here
        obs, _, _, _, _ = env.step(actions)
        env.render()


if __name__ == "__main__":
    main()
