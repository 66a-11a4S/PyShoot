import pygame
from enemy_patterns.move_patterns.move_pattern import MovePattern


# 水平に等速直線移動
class HorizontalMove(MovePattern):
    def __init__(self, speed):
        super().__init__()
        self._speed = speed

    def move(self, _):
        return pygame.Vector2(-self._speed, 0)
