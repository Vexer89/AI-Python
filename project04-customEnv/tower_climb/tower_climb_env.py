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
        self._gravity = -1.5
        self._horizontal_speed = 15.0
        self._jump_force = 30.0

        self.map_change_count = 0

        self._platforms = self._initialize_map()

        self._agent_position = np.array([self.map_width / 2, 0], dtype=np.float32)
        self._agent_platform = 0
        self.is_agent_on_platform = True
        self.steps_since_last_platform_change = 0

        self.observation_space = gym.spaces.Dict(
            {
                "agent_position": gym.spaces.Box(
                    low=np.array([0, 0], dtype=np.float32),
                    high=np.array([self.map_width, self.map_height], dtype=np.float32),
                    dtype=np.float32,
                ),
                "current_platform": gym.spaces.Box(
                    low=np.array([0, 0, 0, 0], dtype=np.float32),
                    high=np.array(
                        [self.map_width, self.map_height, self.map_width, self.map_height],
                        dtype=np.float32,
                    ),
                    dtype=np.float32,
                ),
                "next_platform": gym.spaces.Box(
                    low=np.array([0, 0, 0, 0], dtype=np.float32),
                    high=np.array(
                        [self.map_width, self.map_height, self.map_width, self.map_height],
                        dtype=np.float32,
                    ),
                    dtype=np.float32,
                ),
                "agent_speed": gym.spaces.Box(
                    low=-np.inf, high=np.inf, shape=(1,), dtype=np.float64
                ),
            }
        )

        self.action_space = gym.spaces.Discrete(3)

    def _initialize_map(self):
        dist_between_platforms = self.map_height / (self.num_platforms + 1)
        min_width = self.map_width / 8
        max_width = self.map_width / 3

        platforms = np.zeros((self.num_platforms, 2, 2), dtype=np.float32)

        platforms[0, 0] = [self.map_width / 3, 0.0]
        platforms[0, 1] = [2 * (self.map_width / 3), 0.0]

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
                self._agent_velocity_y <= 0 and abs(self._agent_position[1] - y) < 8
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
            "next_platform": self._platforms[
                min(self._agent_platform + 1, self.num_platforms - 1)
            ].flatten(),
            "agent_speed": np.array([self._agent_velocity_y], dtype=np.float64),
        }

    def _get_info(self):
        return {"platform": self._agent_platform}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self._agent_position = np.array([self.map_width / 2, 0], dtype=np.float32)
        self._agent_velocity_y = 0.0
        self._agent_platform = 0
        self.is_agent_on_platform = True

        if self.map_change_count > 50:
            self._platforms = self._initialize_map()
            self.map_change_count = 0
        else:
            self.map_change_count += 1

        return self._get_obs(), self._get_info()

    def step(self, action):
        terminated = False
        truncated = False
        reward = 0.0

        # Ruch poziomy
        if action == Actions.left.value:
            self._agent_position[0] = max(0.0, self._agent_position[0] - self._horizontal_speed)
        elif action == Actions.right.value:
            self._agent_position[0] = min(self.map_width, self._agent_position[0] + self._horizontal_speed)
        elif action == Actions.jump.value:
            if self.is_agent_on_platform:
                self._agent_velocity_y = self._jump_force
                self.is_agent_on_platform = False
                reward += 1.0  # Niewielka nagroda za skok
            else:
                reward -= 0.2  # Mniejsza kara za skok w powietrzu

        # Grawitacja
        if not self.is_agent_on_platform:
            self._agent_velocity_y += self._gravity

        self._agent_position[1] += self._agent_velocity_y
        self._agent_position[1] = max(self._agent_position[1], 0)

        last_platform = self._agent_platform
        self.is_agent_on_platform = self._agent_on_platform()

        # Awans na wyższą platformę
        if self._agent_platform > last_platform:
            reward += 100.0
            self.steps_since_last_platform_change = 0
        elif self._agent_platform < last_platform:
            reward -= 50.0  # Mniejsza kara za spadek
            self.steps_since_last_platform_change = 0
        else:
            self.steps_since_last_platform_change += 1

        # Kara za stagnację
        if self.steps_since_last_platform_change > 15:
            reward -= 1.0  # Delikatniejsza kara

        # Nagroda za zbliżanie się do centrum następnej platformy
        next_platform_idx = min(self._agent_platform + 1, self.num_platforms - 1)
        next_x1, next_y1 = self._platforms[next_platform_idx][0]
        next_x2, next_y2 = self._platforms[next_platform_idx][1]
        next_center = np.array([(next_x1 + next_x2) / 2, (next_y1 + next_y2) / 2])
        agent_pos = np.array(self._agent_position)

        distance = np.linalg.norm(agent_pos - next_center)
        max_possible_distance = np.sqrt(self.map_width ** 2 + self.map_height ** 2)
        proximity_reward = 10.0 * (1 - distance / max_possible_distance)
        reward += proximity_reward

        # Nowość: nagroda za poruszanie się w kierunku X wyższej platformy
        if agent_pos[0] < next_center[0]:
            reward += 0.2  # Delikatna nagroda za ruch w prawo
        else:
            reward += 0.1  # Delikatna nagroda za ruch w lewo (żeby było neutralnie)

        # Kara za przebywanie na ziemi
        if self._agent_position[1] < 500:
            reward -= 0.05

        # Nagroda za wysokość
        reward += 0.1 * (self._agent_position[1] / self.map_height)  # Skalowanie do mapy

        # Kara za spadnięcie poniżej mapy
        if self._agent_position[1] <= 0:
            reward -= 500.0
            terminated = True

        # Nagroda za osiągnięcie ostatniej platformy
        if self._agent_platform == self.num_platforms - 1:
            reward += 500.0
            terminated = True

        return self._get_obs(), float(reward), terminated, truncated, self._get_info()

    def render(self):
        if self.render_mode == "ansi":
            print(f"Is agent on platform: {self.is_agent_on_platform}")
            print(f"Current platform index: {self._agent_platform}")
            print(f"Next platform index: {min(self._agent_platform + 1, self.num_platforms - 1)}")
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
                    5,
                )
                pygame.draw.rect(self.window, (255, 255, 255), rect)

            agent_rect = pygame.Rect(
                int(self._agent_position[0] * self.scale - 5),
                int(self.window_size[1] - self._agent_position[1] * self.scale - 10),
                10,
                10,
            )

            pygame.draw.rect(self.window, (0, 255, 0), agent_rect)

            pygame.display.flip()
            self.clock.tick(30)

    def close(self):
        if self.window is not None:
            pygame.quit()
            self.window = None
