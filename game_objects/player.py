import pygame
from game_objects import game_object, bullet
from collision import sphere_collider
# from collision import box_collider
from collision.collision_layer import CollisionLayer
from object_pool import ObjectPool


class Player(game_object.GameObject):
    _shoot_interval = 0.05

    def __init__(self, position, scroll_velocity, screen_size):
        super().__init__()
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

        bullet_factory = lambda: bullet.Bullet()
        self._bullet_pool = ObjectPool(bullet_factory, init_size=64)
        self._shoot_timer = 0.0

    def update(self, dt):
        # reset state
        self._intersecting = False

        keys = pygame.key.get_pressed()
        self.update_position(keys, dt)
        self.update_shoot(keys, dt)

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

    def update_position(self, keys, dt):
        velocity = pygame.Vector2()

        # プレイヤーが移動できる画面内の領域
        boundary_max = self.screen_size + velocity
        boundary_min = velocity

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

    def update_shoot(self, keys, dt):
        if keys[pygame.K_SPACE]:
            if self._shoot_timer == 0.0:
                self.shoot()

            self._shoot_timer += dt

            if self._shoot_interval < self._shoot_timer:
                self._shoot_timer = 0.0
        else:
            self._shoot_timer = 0.0

    def shoot(self):
        instance = self._bullet_pool.rent()
        instance.setup(pygame.Vector2(self.position), pygame.Vector2(512, 0), pygame.Vector2(16, 16), True,
                       self._bullet_pool)
