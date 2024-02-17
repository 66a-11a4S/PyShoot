import pygame

import game_object


class Camera(game_object.GameObject):
    def __init__(self, upper_left, size):
        self.position = upper_left
        self.size = size
        self.scroll_velocity = pygame.Vector2(32, 0)

    def update(self, dt):
        self.position += self.scroll_velocity * dt

    def draw(self, screen, camera_position):
        pass
