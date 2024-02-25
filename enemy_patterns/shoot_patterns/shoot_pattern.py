import pygame


class ShootPattern:
    def __init__(self, interval):
        self.interval = interval
        self._owner_position = pygame.Vector2()
        self._target_position = pygame.Vector2()

    def setup(self, owner_position, target_position):
        self._owner_position = owner_position
        self._target_position = target_position

    def tick(self, timer):
        # clamped_timer == interval になった瞬間のみ発射
        return self.interval <= timer
