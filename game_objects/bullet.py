import pygame

import app_setting
from collision.collision_layer import CollisionLayer
from collision.sphere_collider import SphereCollider
from game_objects import game_object


class Bullet(game_object.GameObject):
    def __init__(self):
        super().__init__()
        self.material = None
        self.velocity = pygame.Vector2()
        self.position = pygame.Vector2()
        self._radius = 0
        self.collider = None
        self.is_player_bullet = False
        self.enabled = False
        self._pool = None
        self._image = None

    def setup(self, position, velocity, size, is_player_bullet, pool):
        self.position = position
        self.velocity = velocity
        self._radius = size.x
        layer = CollisionLayer.PlayerShot if is_player_bullet else CollisionLayer.EnemyShot
        self.collider = SphereCollider(self.position, self._radius, self.on_intersected, layer)
        self.material = pygame.Color(128, 255, 255) if is_player_bullet else pygame.Color(255, 128, 255)
        image_path = "resource/image/player_bullet.png" if is_player_bullet else "resource/image/enemy_bullet.png"
        self._image = pygame.image.load(image_path)
        self._pool = pool

        self.collider.enabled = True
        self.enabled = True

    def on_intersected(self, _):
        self.disable()

    def update(self, dt):
        if not app_setting.is_in_screen(self.position):
            self.disable()
            return

        self.position += self.velocity * dt

    def draw(self, screen, camera_position):
        # pygame.draw.circle(screen, self.material, self.position, self._radius)
        view_position = self.position - pygame.Vector2(self._radius, self._radius)
        screen.blit(self._image, view_position)

    def disable(self):
        self.collider.enabled = False
        self.enabled = False
        if self._pool is not None:
            self._pool.back(self)
