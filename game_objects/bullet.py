import pygame

from collision.collision_layer import CollisionLayer
from collision.sphere_collider import SphereCollider
from game_objects import game_object


class Bullet(game_object.GameObject):
    def __init__(self, start_at, size, velocity, is_player_bullet):
        self._velocity = velocity
        self.position = start_at
        self.is_player_bullet = is_player_bullet
        self.radius = size.x
        self.material = pygame.Color(128, 255, 255) if self.is_player_bullet else pygame.Color(255, 255, 128)

        layer = CollisionLayer.PlayerShot if is_player_bullet else CollisionLayer.EnemyShot
        self.collider = SphereCollider(self.position, self.radius, self.on_intersected, layer)

    def on_intersected(self, _):
        self.collider.enabled = False

    def update(self, dt):
        self.position += self._velocity * dt

    def draw(self, screen, camera_position):
        pygame.draw.circle(screen, self.material, self.position, self.radius)
