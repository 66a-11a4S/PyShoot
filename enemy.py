import random
import pygame
import game_object


class Enemy(game_object.GameObject):
    def __init__(self):
        self.position = pygame.Vector2(random.randint(0, 640), random.randint(0, 480))
        self._size = pygame.Vector2(32, 32)
        self.material = pygame.Color(255, 128, 128)

    def update(self, dt):
        pass

    def draw(self, screen, camera_position):
        min_pos = self.position - self._size / 2
        enemy_view_pos = min_pos - camera_position
        rect = pygame.Rect(enemy_view_pos.x, enemy_view_pos.y, self._size.x, self._size.y)
        pygame.draw.rect(screen, self.material, rect)
