import pygame
import app_setting
from collision.collision_layer import CollisionLayer
from collision.sphere_collider import SphereCollider
from game_objects import game_object


class Bullet(game_object.GameObject):
    def __init__(self, is_player_bullet):
        super().__init__()
        self.material = None
        self.velocity = pygame.Vector2()
        self.position = pygame.Vector2()
        self._radius = 0
        layer = CollisionLayer.PlayerShot if is_player_bullet else CollisionLayer.EnemyShot
        self.collider = SphereCollider(pygame.Vector2(), 1, self.on_intersected, layer)
        self.enabled = False
        self._pool = None

        # self.material = pygame.Color(128, 255, 255) if is_player_bullet else pygame.Color(255, 128, 255)
        image_path = "resource/image/player_bullet.png" if is_player_bullet else "resource/image/enemy_bullet.png"
        self._image = pygame.image.load(image_path)

    def setup(self, position, velocity, size, pool):
        self.position = position
        self.velocity = velocity
        self._radius = size.x
        self.collider.center = self.position
        self.collider.size.x = self._radius
        self.collider.size.y = self._radius
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
