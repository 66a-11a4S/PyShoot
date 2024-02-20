import random
import pygame
import game_object
from collision import box_collider
from collision.collision_layer import CollisionLayer


class Enemy(game_object.GameObject):
    def __init__(self):
        self.position = pygame.Vector2(random.randint(0, 640), random.randint(0, 480))
        self._size = pygame.Vector2(32, 32)
        self.material = pygame.Color(255, 128, 128)
        self.collider = box_collider.BoxCollider(self.position, self._size, self.on_intersected, CollisionLayer.Enemy)
        self._intersecting = False
        self._velocity = pygame.Vector2(-32, 0)

    def update(self, dt):
        self._intersecting = False
        self.position += self._velocity * dt

    def draw(self, screen, camera_position):
        min_pos = self.position - self._size / 2
        enemy_view_pos = min_pos
        rect = pygame.Rect(enemy_view_pos.x, enemy_view_pos.y, self._size.x, self._size.y)
        mat = pygame.Color(0, 0, 0) if self._intersecting else self.material
        pygame.draw.rect(screen, mat, rect)

    def on_intersected(self, _):
        self._intersecting = True
