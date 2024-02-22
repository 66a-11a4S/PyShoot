import pygame

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
        self._previous_camera_position = pygame.Vector2()

    def setup(self, position, velocity, size, is_player_bullet):
        self.position = position
        self.velocity = velocity
        self._radius = size.x
        layer = CollisionLayer.PlayerShot if is_player_bullet else CollisionLayer.EnemyShot
        self.collider = SphereCollider(self.position, self._radius, self.on_intersected, layer)
        self.material = pygame.Color(128, 255, 255) if self.is_player_bullet else pygame.Color(255, 255, 128)

        self.collider.enabled = True
        self.enabled = True

    def on_intersected(self, _):
        self.collider.enabled = False
        self.enabled = False

    def update(self, dt):
        view_position = self.position - self._previous_camera_position
        if 640 < view_position.x:
            self.dispose()
            return

        self.position += self.velocity * dt

    def draw(self, screen, camera_position):
        pygame.draw.circle(screen, self.material, self.position, self._radius)
        self._previous_camera_position = camera_position
