import random
import pygame
import game_object
import box_collider


class Enemy(game_object.GameObject):
    def __init__(self):
        self.position = pygame.Vector2(random.randint(0, 640), random.randint(0, 480))
        self._size = pygame.Vector2(32, 32)
        self.material = pygame.Color(255, 128, 128)
        self.collider = box_collider.BoxCollider(self.position, self._size, self.on_intersected)
        self._intersecting = False

    def update(self, dt):
        self._intersecting = False

    def draw(self, screen, camera_position):
        min_pos = self.position - self._size / 2
        enemy_view_pos = min_pos - camera_position
        rect = pygame.Rect(enemy_view_pos.x, enemy_view_pos.y, self._size.x, self._size.y)
        mat = pygame.Color(0, 0, 0) if self._intersecting else self.material
        pygame.draw.rect(screen, mat, rect)

    def on_intersected(self, _):
        self._intersecting = True
