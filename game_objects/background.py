import pygame
from game_objects.game_object import GameObject


class Background(GameObject):
    def __init__(self, scroll_speed):
        super().__init__()
        self._image = pygame.image.load("resource/image/background.png")
        self._scroll_speed = scroll_speed
        self._scroll_position = 0
        self._scroll_end = self._image.get_width()

    def update(self, dt):
        self._scroll_position += self._scroll_speed * dt
        self._scroll_position %= self._scroll_end

    def draw(self, screen, _):
        position = pygame.Vector2(-self._scroll_position, 0)
        screen.blit(self._image, position)
        position.x += self._scroll_end
        screen.blit(self._image, position)
