import random
import pygame

from enemy_patterns.interval_pattern import IntervalPattern
from enemy_patterns.move_patterns.chase import Chase
from enemy_patterns.move_patterns.horizontal_move import HorizontalMove
from enemy_patterns.move_patterns.vertical_chase import VerticalChase
from enemy_patterns.move_patterns.wave import Wave
from game_objects import game_object
from collision import box_collider
from collision.collision_layer import CollisionLayer


class Enemy(game_object.GameObject):
    def __init__(self):
        super().__init__()
        self.position = pygame.Vector2(random.randint(0, 640), random.randint(0, 480))
        self._size = pygame.Vector2(32, 32)
        self.material = pygame.Color(255, 128, 128)
        self.collider = box_collider.BoxCollider(self.position, self._size, self.on_intersected, CollisionLayer.Enemy)
        self._intersecting = False

        interval = 1
        # move_pattern = HorizontalMove(-64)
        # move_pattern = Wave(-64, 256, interval)
        # move_pattern = Chase(self.position, target_position=pygame.Vector2(320, 320), speed=1, stop_distance=64)
        move_pattern = VerticalChase(self.position, target_position=pygame.Vector2(0, 320),
                                     velocity=pygame.Vector2(-256, 32))
        self._move_pattern = IntervalPattern(interval, move_pattern.move)

    def update(self, dt):
        self._intersecting = False
        velocity = self._move_pattern.update(dt)
        self.position += velocity * dt

    def draw(self, screen, camera_position):
        min_pos = self.position - self._size / 2
        enemy_view_pos = min_pos
        rect = pygame.Rect(enemy_view_pos.x, enemy_view_pos.y, self._size.x, self._size.y)
        mat = pygame.Color(0, 0, 0) if self._intersecting else self.material
        pygame.draw.rect(screen, mat, rect)

    def on_intersected(self, collider):
        self._intersecting = True
        if collider.layer == CollisionLayer.PlayerShot:
            self.enabled = False
            self.collider.enabled = False
