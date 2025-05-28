from enum import Enum
import numpy as np
import gymnasium as gym
import pygame


class Actions(Enum):
    left = 0
    right = 1
    jump = 2

class TowerClimbEnv(gym.Env):
    metadata = {"render_modes": ["human", "ansi"]}

    def __init__(self, render_mode="ansi"):

        self.render_mode = render_mode
        self.window_size = (600, 600)
        self.scale = self.window_size[0] / 900  # for drawing
        self.window = None
        self.clock = None

        self.map_width = 900
        self.map_height = 900
        self.num_platforms = 5

        self._agent_velocity_y = 0.0
        self._gravity = -2.0
        self._horizontal_speed = 10.0
        self._jump_force = 30.0

        self._platforms = self._initialize_map()

        #TODO: agent position on platform
        self._agent_position = np.array([self.map_width / 2, 0], dtype=np.float32)
        self._agent_platform = 0
        self.is_agent_on_platform = True

        self.observation_space = gym.spaces.Dict(
            {
                "agent_position": gym.spaces.Box(
                    low=np.array([0, 0], dtype=np.float32),
                    high=np.array([self.map_width, self.map_height], dtype=np.float32),
                    dtype=np.float32
                ),
                "current_platform": gym.spaces.Box(
                    low=np.array([0, 0, 0,0], dtype=np.float32),
                    high=np.array(
                        [self.map_width, self.map_height, self.map_width, self.map_height],
                        dtype=np.float32),
                    dtype=np.float32
                ),
                "next_platform": gym.spaces.Box(
                    low=np.array([0, 0, 0,0], dtype=np.float32),
                    high=np.array(
                        [self.map_width, self.map_height, self.map_width, self.map_height],
                        dtype=np.float32),
                    dtype=np.float32
                )
            }
        )

        self.action_space = gym.spaces.Discrete(3)

    def _initialize_map(self):
        dist_between_platforms = self.map_height / (self.num_platforms + 1)
        min_width = self.map_width / 8
        max_width = self.map_width / 3

        platforms = np.zeros((self.num_platforms, 2, 2), dtype=np.float32)
        # [[0,0], [1, 1]]
        # [[0,0], [2,2]]
        # 1:: 1:1:

        platforms[0, 0] = [0.0, 0.0]
        platforms[0, 1] = [self.map_width, 0.0]

        for i in range(1, self.num_platforms):
            y = i * dist_between_platforms
            platform_width = np.random.uniform(min_width, max_width)
            x_start = np.random.uniform(0, self.map_width - platform_width)
            x_end = min(x_start + platform_width, self.map_width)

            platforms[i, 0] = [x_start, y]
            platforms[i, 1] = [x_end, y]

        return platforms

    def _agent_on_platform(self):
        for i in range(self.num_platforms):
            x1, y = self._platforms[i, 0]
            x2, _ = self._platforms[i, 1]

            on_x = x1 <= self._agent_position[0] <= x2
            just_above = (
                    self._agent_velocity_y <= 0 and
                    abs(self._agent_position[1] - y) < 5
            )

            if on_x and just_above:
                self._agent_position[1] = y
                self._agent_velocity_y = 0
                self._agent_platform = i
                return True
        return False

    def _get_obs(self):
        return {
            "agent_position": self._agent_position.copy(),
            "current_platform": self._platforms[self._agent_platform].flatten(),
            "next_platform": self._platforms[min(self._agent_platform + 1, self.num_platforms - 1)].flatten()
        }

    def _get_info(self):
        return {
            "platform" : self._agent_platform
        }

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self._agent_position = np.array([self.map_width / 2, 0], dtype=np.float32)
        self._agent_velocity_y = 0.0
        self._agent_platform = 0
        self.is_agent_on_platform = True
        self._platforms = self._initialize_map()

        return self._get_obs(), self._get_info()

    def step(self, action):
        terminated = False
        truncated = False

        if action == Actions.left.value:
            move = max(0.0, self._agent_position[0] - self._horizontal_speed)
            self._agent_position[0] = move
        elif action == Actions.right.value:
            move = min(self.map_width, self._agent_position[0] + self._horizontal_speed)
            self._agent_position[0] = move
        elif action == Actions.jump.value:
            if self.is_agent_on_platform:
                self._agent_velocity_y = self._jump_force

        if not self.is_agent_on_platform:
            self._agent_velocity_y += self._gravity

        self._agent_position[1] += self._agent_velocity_y

        last_platform = self._agent_platform

        self.is_agent_on_platform = self._agent_on_platform()

        if self._agent_platform > last_platform:
            reward = 2
        elif self._agent_platform < last_platform:
            reward = -10
        else:
            reward = 0

        if self._agent_platform == self.num_platforms:
            terminated = True
            reward = 20

        return self._get_obs(), reward, terminated, truncated, self._get_info()

    def render(self):
        if self.render_mode == "ansi":
            print(f"Agent position: {self._agent_position}")
            print(f"Velocity Y: {self._agent_velocity_y}")
            print("Platforms:")
            for i, p in enumerate(self._platforms):
                print(f"{i}: {p[0]} -> {p[1]}")
        elif self.render_mode == "human":
            if self.window is None:
                pygame.init()
                self.window = pygame.display.set_mode(self.window_size)
                pygame.display.set_caption("Tower Climb")
                self.clock = pygame.time.Clock()

            self.window.fill((0, 0, 0))  # black background

            # Draw platforms
            for p in self._platforms:
                x1, y = map(float, p[0])
                x2 = float(p[1][0])
                rect = pygame.Rect(
                    int(x1 * self.scale),
                    int(self.window_size[1] - y * self.scale),
                    int((x2 - x1) * self.scale),
                    5
                )
                pygame.draw.rect(self.window, (255, 255, 255), rect)

            agent_rect = pygame.Rect(
                int(self._agent_position[0] * self.scale - 5),
                int(self.window_size[1] - self._agent_position[1] * self.scale - 10),
                10, 10
            )

            pygame.draw.rect(self.window, (0, 255, 0), agent_rect)

            pygame.display.flip()
            self.clock.tick(30)

    def close(self):
        if self.window is not None:
            pygame.quit()
            self.window = None



