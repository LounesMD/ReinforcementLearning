from gymnasium.envs.registration import register

register(
    id="env_DAv-v0",
    entry_point="Codes.Gym_envs.DAv.env_DAv:Env_DAv",
)

register(
    id="env_cartPole-v0",
    entry_point="Codes.Gym_envs.CartPole.env_CartPole:Env_CartPole",
)
