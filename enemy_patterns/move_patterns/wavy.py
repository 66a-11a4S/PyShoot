import math
import pygame
from enemy_patterns.move_patterns.move_pattern import MovePattern


# 横方向に等速, 縦方向に sin
class Wavy(MovePattern):
    def __init__(self, horizontal_speed, amp, duration):
        super().__init__()
        self._horizontal_speed = horizontal_speed
        self._amp = amp
        self._interval = duration

    def move(self, timer):
        y = math.sin(timer / self.interval * math.pi * 2) * self._amp
        return pygame.Vector2(-self._horizontal_speed, y)
