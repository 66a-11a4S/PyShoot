import pygame

from enemy_patterns.interval_pattern import IntervalPattern


class SpriteAnimation:
    def __init__(self, path, size, duration):
        self._image = pygame.image.load(path)
        self._size = size
        self._sprite_count = self._image.get_width() // size.x

        # surface_rect の範囲だけ描画するように設定
        self._surface_rect = pygame.Rect(0, 0, size.x, size.y)

        self._is_playing = False
        self._has_finished = False
        self._sprite_index = 0

        interval = duration / self._sprite_count
        self._interval = IntervalPattern(interval, self.next_sprite)

    def play(self):
        self._sprite_index = 0
        self._interval.reset()
        self._is_playing = True
        self._has_finished = False

    def update(self, dt):
        if self._is_playing:
            self._interval.update(dt)

    def next_sprite(self, timer):
        if timer < self._interval.duration:
            return

        if self._sprite_index < self._sprite_count - 1:
            self._sprite_index += 1
            self._surface_rect.x = self._size.x * self._sprite_index
            self._interval.reset()
        else:
            self._is_playing = False
            self._has_finished = True

    @property
    def surface_rect(self):
        return self._surface_rect

    @property
    def image(self):
        return self._image

    @property
    def is_playing(self):
        return self._is_playing

    @property
    def has_finished(self):
        return self._has_finished
