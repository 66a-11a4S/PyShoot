import pygame

import app_setting
from game_objects import game_object
from collision import box_collider
from collision.collision_layer import CollisionLayer


class Enemy(game_object.GameObject):
    def __init__(self, bullet_pool):
        super().__init__()
        self._bullet_pool = bullet_pool
        self._size = pygame.Vector2(32, 32)
        self.material = pygame.Color(255, 128, 128)
        self._disappear_range_margin = self._size

        self.position = pygame.Vector2()
        self._move_pattern = None
        self._shoot_pattern = None
        self.collider = box_collider.BoxCollider(self.position, self._size, self.on_intersected, CollisionLayer.Enemy)

        self.disable()

    def setup(self, position, move_pattern, shoot_pattern, player_pos):
        self.position = position
        self._move_pattern = move_pattern
        self._shoot_pattern = shoot_pattern

        self.collider.center = position
        self.collider.enabled = True
        self.enabled = True

    def update(self, dt):
        velocity = self._move_pattern.update(dt)
        self.position += velocity * dt

        if not app_setting.is_in_screen(self.position, margin=self._disappear_range_margin):
            self.disable()
            return

        shoot_requests = self._shoot_pattern.update(dt)
        for request in shoot_requests:
            self.shoot(request)

    def draw(self, screen, camera_position):
        min_pos = self.position - self._size / 2
        enemy_view_pos = min_pos
        rect = pygame.Rect(enemy_view_pos.x, enemy_view_pos.y, self._size.x, self._size.y)
        pygame.draw.rect(screen, self.material, rect)

    def on_intersected(self, collider):
        if collider.layer == CollisionLayer.PlayerShot:
            self.disable()

    def shoot(self, vec):
        instance = self._bullet_pool.rent()
        instance.setup(pygame.Vector2(self.position), vec, pygame.Vector2(4, 4), False, self._bullet_pool)

    def disable(self):
        self.collider.enabled = False
        self.enabled = False
