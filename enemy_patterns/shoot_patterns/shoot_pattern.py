import pygame


class ShootPattern:
    def __init__(self):
        self._owner_position = pygame.Vector2()
        self._target_position = pygame.Vector2()

    def setup(self, owner_position, target_position):
        self._owner_position = owner_position
        self._target_position = target_position
