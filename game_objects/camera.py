import pygame

from game_objects import game_object


class Camera(game_object.GameObject):
    def __init__(self, upper_left):
        super().__init__()
        self.position = upper_left
        self._scroll_velocity = pygame.Vector2(32, 0)

    def update(self, dt):
        self.position += self._scroll_velocity * dt

    def draw(self, screen, camera_position):
        pass
