import random
import pygame

from enemy_patterns.interval_pattern import IntervalPattern
from enemy_patterns.move_patterns.chase import Chase
from enemy_patterns.move_patterns.horizontal_move import HorizontalMove
from enemy_patterns.move_patterns.vertical_chase import VerticalChase
from enemy_patterns.move_patterns.wave import Wave
from enemy_patterns.shoot_patterns.front import Front
from enemy_patterns.shoot_patterns.target_centric import TargetCentric
from game_objects import game_object
from collision import box_collider
from collision.collision_layer import CollisionLayer
from game_objects.bullet import Bullet
from object_pool import ObjectPool


class Enemy(game_object.GameObject):
    def __init__(self):
        super().__init__()
        self.position = pygame.Vector2(random.randint(320, 640), random.randint(0, 480))
        self._size = pygame.Vector2(32, 32)
        self.material = pygame.Color(255, 128, 128)
        self.collider = box_collider.BoxCollider(self.position, self._size, self.on_intersected, CollisionLayer.Enemy)
        self._intersecting = False

        move_interval = 3
        # move_pattern = HorizontalMove(-16.0)
        move_pattern = Wave(-128, 64, move_interval)
        # move_pattern = Chase(self.position, target_position=pygame.Vector2(320, 320), speed=1, stop_distance=64)
        # move_pattern = VerticalChase(self.position, target_position=pygame.Vector2(0, 320),
        #                              velocity=pygame.Vector2(-256, 32))
        self._move_pattern = IntervalPattern(move_interval, move_pattern.move)

        shoot_interval = 0.5
        # shoot_pattern = TargetCentric(shoot_interval, self.position, target_position=pygame.Vector2(0, 320), speed=128,
        #                              ways=1, angle=0)
        shoot_pattern = Front(shoot_interval, self.position, speed=256, ways=5, angle=15)
        self._shoot_pattern = IntervalPattern(shoot_interval, shoot_pattern.shoot)
        self._bullet_pool = ObjectPool(lambda: Bullet())

    def update(self, dt):
        self._intersecting = False
        velocity = self._move_pattern.update(dt)
        self.position += velocity * dt

        shoot_requests = self._shoot_pattern.update(dt)
        for request in shoot_requests:
            self.shoot(request)

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

    def shoot(self, vec):
        instance = self._bullet_pool.rent()
        instance.setup(pygame.Vector2(self.position), vec, pygame.Vector2(4, 4), False, self._bullet_pool)
