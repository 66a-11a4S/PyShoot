import pygame


# 水平に等速直線移動
class HorizontalMove:
    def __init__(self, horizontal_speed):
        self._speed = horizontal_speed

    def move(self, _):
        return pygame.Vector2(self._speed, 0)
