from gymnasium.envs.registration import register

register(
    id="icy_tower_env/GridWorld-v0",
    entry_point="icy_tower_env.envs:GridWorldEnv",
)
