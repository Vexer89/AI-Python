from tower_climb.tower_climb_env import TowerClimbEnv

env = TowerClimbEnv(render_mode="human")  # lub "ansi"
obs, info = env.reset()
done = False
while not done:
    action = env.action_space.sample()
    obs, reward, done, _, info = env.step(action)
    env.render()
env.close()
