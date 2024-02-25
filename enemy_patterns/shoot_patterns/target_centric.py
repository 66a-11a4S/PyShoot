import math
import pygame
from enemy_patterns.shoot_patterns.shoot_pattern import ShootPattern


# 特定の位置を基準とする
class TargetCentric(ShootPattern):
    def __init__(self, speed, interval, ways, angle):
        super().__init__(interval)
        self._speed = speed
        self._ways = ways
        self._angle = angle

    def shoot(self, timer):
        requests = []

        if not self.tick(timer):
            return requests

        if self._ways % 2 == 1:
            raw_vec = (self._target_position - self._owner_position)
            vec = raw_vec * self._speed / (raw_vec.length() + 0.1)
            requests.append(vec)

        for idx in range(1, int(self._ways / 2) + 1):
            raw_vec = (self._target_position - self._owner_position)
            vec = raw_vec * self._speed / (raw_vec.length() + 0.1)
            angle = self._angle * idx / (self._ways - 1)
            vec_left = pygame.Vector2(vec).rotate_rad(math.pi * angle / 180)
            requests.append(vec_left)
            vec_right = pygame.Vector2(vec).rotate_rad(-math.pi * 2.0 * angle / 360)
            requests.append(vec_right)

        return requests
