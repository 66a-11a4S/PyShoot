# 縦軸だけ合わせて通りすぎる
import pygame


class VerticalChase:
    def __init__(self, owner_position, target_position, velocity):
        self._owner_position = owner_position
        self._target_position = target_position
        self._velocity = velocity

    def move(self, _):
        diff = self._target_position.y - self._owner_position.y
        vy = min(self._velocity.y, diff)
        return pygame.Vector2(self._velocity.x, vy)
