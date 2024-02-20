import pygame
import game_object
from collision import sphere_collider
# from collision import box_collider
from collision.collision_layer import CollisionLayer


class Player(game_object.GameObject):
    def __init__(self, position, scroll_velocity, screen_size):
        self.position = position
        self.material = pygame.Color(128, 128, 255)
        self.shape = 32  # circle radius
#        self._size = pygame.Vector2(32, 32)
        self.move_speed = 256
        self.scroll_velocity = scroll_velocity
        self.screen_size = screen_size
        self.collider = sphere_collider.SphereCollider(self.position, self.shape, self.on_intersected,
                                                       CollisionLayer.Player)
#        self.collider = box_collider.BoxCollider(self.position, self._size, self.on_intersected)
        self._intersecting = False

    def update(self, dt):

        # reset state
        self._intersecting = False

        velocity = pygame.Vector2()

        # プレイヤーが移動できる画面内の領域
        boundary_max = self.screen_size + velocity
        boundary_min = velocity

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            velocity.y -= self.move_speed * dt
        if keys[pygame.K_s]:
            velocity.y += self.move_speed * dt
        if keys[pygame.K_a]:
            velocity.x -= self.move_speed * dt
        if keys[pygame.K_d]:
            velocity.x += self.move_speed * dt

        moved_position = self.position + velocity
        if boundary_max.x < moved_position.x:
            velocity.x = boundary_max.x - self.position.x
        if moved_position.x < boundary_min.x:
            velocity.x = boundary_min.x - self.position.x
        if boundary_max.y < moved_position.y:
            velocity.y = boundary_max.y - self.position.y
        if moved_position.y < boundary_min.y:
            velocity.y = boundary_min.y - self.position.y

        self.position += velocity

    def draw(self, screen, camera_position):
        player_view_position = self.position

        mat = pygame.Color(0, 0, 0) if self._intersecting else self.material
        pygame.draw.circle(screen, mat, player_view_position, self.shape)

#        mat = pygame.Color(0, 0, 0) if self._intersecting else self.material
#        min_pos = self.position - self._size / 2
#        enemy_view_pos = min_pos
#        rect = pygame.Rect(enemy_view_pos.x, enemy_view_pos.y, self._size.x, self._size.y)
#        pygame.draw.rect(screen, mat, rect)

    def on_intersected(self, _):
        self._intersecting = True
