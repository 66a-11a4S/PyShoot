import pygame
from enemy_patterns.move_patterns.move_pattern import MovePattern


# 縦軸だけ合わせて通りすぎる
class VerticalChase(MovePattern):
    def __init__(self, speed, vertical_speed):
        super().__init__()
        self._speed = speed
        self._vertical_speed = vertical_speed

    def move(self, _):
        diff = self._target_position.y - self._owner_position.y
        vy = min(self._vertical_speed, diff)
        return pygame.Vector2(-self._speed, vy)
