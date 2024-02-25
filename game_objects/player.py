import pygame
from game_objects import game_object, bullet
from collision import sphere_collider
from collision.collision_layer import CollisionLayer
from object_pool import ObjectPool


class Player(game_object.GameObject):
    _shoot_interval = 0.025
    _bullet_size = pygame.Vector2(6, 6)
    _bullet_velocity = pygame.Vector2(640, 0)
    _move_speed = 256

    def __init__(self, position, scroll_velocity, screen_size):
        super().__init__()
        self.position = position
        self._material = pygame.Color(128, 128, 255)
        self._shape = 16  # circle radius
        self._scroll_velocity = scroll_velocity
        self._move_boundary = screen_size
        self.collider = sphere_collider.SphereCollider(self.position, self._shape, self.on_intersected,
                                                       CollisionLayer.Player)
        self._intersecting = False

        self._bullet_pool = ObjectPool(lambda: bullet.Bullet(), init_size=64)
        self._shoot_timer = 0.0

    def update(self, dt):
        # reset state
        self._intersecting = False

        keys = pygame.key.get_pressed()
        self.update_position(keys, dt)
        self.update_shoot(keys, dt)

    def draw(self, screen, camera_position):
        player_view_position = self.position
        mat = pygame.Color(0, 0, 0) if self._intersecting else self._material
        pygame.draw.circle(screen, mat, player_view_position, self._shape)

    def on_intersected(self, _):
        self._intersecting = True

    def update_position(self, keys, dt):
        velocity = pygame.Vector2()

        if keys[pygame.K_w]:
            velocity.y -= self._move_speed * dt
        if keys[pygame.K_s]:
            velocity.y += self._move_speed * dt
        if keys[pygame.K_a]:
            velocity.x -= self._move_speed * dt
        if keys[pygame.K_d]:
            velocity.x += self._move_speed * dt

        # プレイヤーが移動できる画面内の領域
        boundary_max = self._move_boundary
        boundary_min = pygame.Vector2(0, 0)

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

    def update_shoot(self, keys, dt):
        if keys[pygame.K_SPACE]:
            if self._shoot_timer == 0.0:
                # 2-way shot
                self.shoot(self.position + pygame.Vector2(16, -8))
                self.shoot(self.position + pygame.Vector2(16, 8))

            self._shoot_timer += dt

            if self._shoot_interval < self._shoot_timer:
                self._shoot_timer = 0.0
        else:
            self._shoot_timer = 0.0

    def shoot(self, position):
        instance = self._bullet_pool.rent()
        instance.setup(pygame.Vector2(position), self._bullet_velocity, self._bullet_size, True, self._bullet_pool)
