import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np

class IcyTowerEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self):
        self.action_space = spaces.MultiDiscrete([3, 2])  # [ruch: 0=bez, 1=lewo, 2=prawo], [skok: 0/1]

        # Obserwacja: x, y, vx, vy, dx_to_platform, dy_to_platform
        self.observation_space = spaces.Box(
            low=np.array([-np.inf] * 6),
            high=np.array([np.inf] * 6),
            dtype=np.float32
        )

        self.gravity = -0.5
        self.jump_strength = 10.0
        self.move_speed = 1.0

        self.platform_x = 5.0
        self.platform_y = 10.0
        self.platform_width = 3.0

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.prev_y = 0.0  # do obliczania różnicy wysokości

        self.done = False
        return self._get_obs(), {}

    def _get_obs(self):
        dx = self.platform_x - self.x
        dy = self.platform_y - self.y
        return np.array([self.x, self.y, self.vx, self.vy, dx, dy], dtype=np.float32)

    def step(self, action):
        if self.done:
            raise RuntimeError("Step called after termination.")

        move, jump = action

        # Ruch poziomy
        if move == 0:
            self.vx = 0.0
        elif move == 1:
            self.vx = -self.move_speed
        elif move == 2:
            self.vx = self.move_speed

        # Skok tylko z ziemi
        if jump == 1 and self.y <= 0.01:
            self.vy = self.jump_strength

        # Fizyka
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

        # Nagroda za wzrost wysokości
        delta_y = self.y - self.prev_y
        reward = max(0.0, delta_y)
        self.prev_y = self.y

        # Sprawdzenie warunku zakończenia
        terminated = False
        truncated = False

        # Trafienie w platformę
        if (
                self.platform_y - 0.5 <= self.y <= self.platform_y + 0.5 and
                self.platform_x - self.platform_width / 2 <= self.x <= self.platform_x + self.platform_width / 2 and
                self.vy <= 0
        ):
            reward += 100.0
            terminated = True
            self.done = True

        # Spadnięcie z planszy
        if self.y < -5:
            reward = -100.0
            terminated = True
            self.done = True

        return self._get_obs(), reward, terminated, truncated, {}

    def render(self):
        print(f"Player: x={self.x:.2f}, y={self.y:.2f} | vx={self.vx:.2f}, vy={self.vy:.2f}")

    def close(self):
        pass
