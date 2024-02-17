import pygame


class AppSetting:
    def __init__(self):
        self._frame_rate = 60
        self._screen_size = pygame.Vector2(640, 480)
        self._bg_fill_color = pygame.Color(128, 128, 128)

    # @property 属性をつけると getter としてみなされ、関数呼び出しの () をつけずに値を参照できる
    @property
    def frame_rate(self):
        return self._frame_rate

    @property
    def screen_size(self):
        return self._screen_size

    @property
    def bg_fill_color(self):
        return self._bg_fill_color
