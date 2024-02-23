import math

import pygame
from enemy_patterns.shoot_patterns.target_centric import TargetCentric


class Front(TargetCentric):
    def __init__(self, interval, owner_position, speed, ways, angle):
        self._interval = interval
        self._owner_position = owner_position
        self._speed = speed
        self._ways = ways
        self._angle = angle

    def shoot(self, timer):
        requests = []

        # clamped_timer == interval になった瞬間のみ発射
        if timer < self._interval:
            return requests

        # 正面を基準に撃つ
        target_position = self._owner_position + pygame.Vector2(-1, 0)
        if self._ways % 2 == 1:
            vec = (target_position - self._owner_position).normalize() * self._speed
            requests.append(vec)

        for idx in range(1, int(self._ways / 2) + 1):
            vec = (target_position - self._owner_position).normalize() * self._speed
            angle = self._angle * idx / (self._ways - 1)
            vec_left = pygame.Vector2(vec).rotate_rad(math.pi * angle / 180)
            requests.append(vec_left)
            vec_right = pygame.Vector2(vec).rotate_rad(-math.pi * 2.0 * angle / 360)
            requests.append(vec_right)

        return requests
