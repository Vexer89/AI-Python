from enum import Enum

import numpy as np
import gymnasium as gym


class Actions(Enum):
    left = 0
    right = 1
    jump = 2


class TowerClimbEnv(gym.Env):
    metadata = {"render_modes": ["human", "ansi"]}

    def __init__(self):

        # TODO: verify width and height
        self.map_width = 900
        self.map_height = 900
        self.num_platforms = 5

        self._agent_velocity_y = 0.0
        self._gravity = -2.0
        self._horizontal_speed = 10.0
        self._jump_force = 30.0

        self.platform_buffer_index = 0
        self._platforms_positions = self._initialize_map()

        self._agent_position = np.array([self.map_width / 2, 50], dtype=np.float32)
        self._last_platform_y = self._agent_position[1]

        self.observation_space = gym.spaces.Dict(
            {
                "agent_position": gym.spaces.Box(
                    low=np.array([0, 0], dtype=np.float32),
                    high=np.array([self.map_width, self.map_height], dtype=np.float32),
                    dtype=np.float32
                ),
                "visible_platforms": gym.spaces.Box(
                    low=0.0,
                    high=max(self.map_width, self.map_height),
                    shape=(20,),
                    dtype=np.float32
                )

            }
        )

        self.action_space = gym.spaces.Discrete(3)

    def _initialize_map(self):
        dist_between_platforms = self.map_height / (self.num_platforms + 1)
        min_width = self.map_width / 8
        max_width = self.map_width / 3

        max_platforms = 1000
        platforms = np.zeros((max_platforms, 2, 2), dtype=np.float32)

        platforms[0, 0] = [0.0, 0.0]
        platforms[0, 1] = [self.map_width, 0.0]
        self.platform_buffer_index = 1

        for i in range(1, self.num_platforms + 1):
            y = i * dist_between_platforms
            platform_width = np.random.uniform(min_width, max_width)
            x_start = np.random.uniform(0, self.map_width - platform_width)
            x_end = x_start + platform_width

            platforms[self.platform_buffer_index, 0] = [x_start, y]
            platforms[self.platform_buffer_index, 1] = [x_end, y]
            self.platform_buffer_index += 1

        return platforms

    def _agent_on_platform(self):
        for i in range(self.platform_buffer_index):
            x1, y = self._platforms_positions[i, 0]
            x2, _ = self._platforms_positions[i, 1]

            on_x = x1 <= self._agent_position[0] <= x2
            just_above = (
                    self._agent_velocity_y <= 0 and
                    abs(self._agent_position[1] - y) < 5
            )

            if on_x and just_above:
                self._agent_position[1] = y
                self._agent_velocity_y = 0
                return True
        return False

    def _generate_next_platform(self):
        min_width = self.map_width / 8
        max_width = self.map_width / 3

        platform_width = np.random.uniform(min_width, max_width)
        x_start = np.random.uniform(0, self.map_width - platform_width)
        x_end = x_start + platform_width

        highest_y = np.max(self._platforms_positions[:self.platform_buffer_index, 0, 1])
        y = highest_y + (self.map_height / (self.num_platforms + 1))

        self._platforms_positions[self.platform_buffer_index, 0] = [x_start, y]
        self._platforms_positions[self.platform_buffer_index, 1] = [x_end, y]
        self.platform_buffer_index += 1

    def _get_visible_platforms(self, max_platforms=3):
        agent_y = self._agent_position[1]

        platforms = []
        for i in range(self.platform_buffer_index):
            y = self._platforms_positions[i, 0, 1]
            if y >= agent_y:
                platforms.append(self._platforms_positions[i])

        platforms = sorted(platforms, key=lambda p: p[0][1])

        visible = platforms[:max_platforms]
        while len(visible) < max_platforms:
            visible.append(np.array([[0.0, 0.0], [0.0, 0.0]], dtype=np.float32))

        visible_array = np.array(visible, dtype=np.float32)
        return visible_array.reshape(-1)

    def _get_obs(self):
        return {
            "agent_position": self._agent_position.copy(),
            "visible_platforms": self._get_visible_platforms()
        }

    def _get_info(self):
        pass

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self._agent_position = np.array([self.map_width / 2, 50], dtype=np.float32)
        self._agent_velocity_y = 0.0
        self._last_platform_y = self._agent_position[1]
        self._platforms_positions = self._initialize_map()

        return self._get_obs(), {}

    def step(self, action):
        terminated = False
        reward = 0.0

        if action == Actions.left.value:
            self._agent_position[0] -= self._horizontal_speed
        elif action == Actions.right.value:
            self._agent_position[0] += self._horizontal_speed
        elif action == Actions.jump.value:
            if self._agent_on_platform():
                self._agent_velocity_y = self._jump_force

        self._agent_velocity_y += self._gravity
        self._agent_position[1] += self._agent_velocity_y

        landed = self._agent_on_platform()

        if landed and self._agent_position[1] > self._last_platform_y:
            dy = self._agent_position[1] - self._last_platform_y
            self._platforms_positions[:self.platform_buffer_index, :, 1] -= dy
            self._agent_position[1] -= dy
            self._last_platform_y = self._agent_position[1]
            self._generate_next_platform()
            reward = 1.0

        if self._agent_position[1] < 0:
            terminated = True
            reward = -10.0

        return self._get_obs(), reward, terminated, False, {}

    def render(self):
        print(f"Agent position: {self._agent_position}")
        print(f"Velocity Y: {self._agent_velocity_y}")
        print(f"Platforms (top 5):")
        for i in range(min(5, self.platform_buffer_index)):
            p = self._platforms_positions[i]
            print(f"  {i}: {p[0]} -> {p[1]}")



