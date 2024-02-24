import math
import pygame


# 横方向に等速, 縦方向に sin
class Wavy:
    def __init__(self, horizontal_speed, amp, duration):
        self._horizontal_speed = horizontal_speed
        self._amp = amp
        self._duration = duration

    def move(self, timer):
        y = math.sin(timer / self._duration * math.pi * 2) * self._amp
        return pygame.Vector2(-self._horizontal_speed, y)
