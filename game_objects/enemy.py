import pygame
import app_setting
from animation.animation_object import AnimationObject
from animation.sprite_animation import SpriteAnimation
from game_objects import game_object
from collision import box_collider
from collision.collision_layer import CollisionLayer


class Enemy(game_object.GameObject):
    _bullet_size = pygame.Vector2(4, 4)

    def __init__(self, bullet_pool):
        super().__init__()
        self._bullet_pool = bullet_pool
        self.material = pygame.Color(255, 128, 128)
        self._image = None
        self._size = pygame.Vector2(0, 0)
        self._disappear_range_margin = self._size

        # HACK: 生成直後、位置更新前に衝突判定が走ってしまうので画面左上に居るとぶつかるのを避けるため画面外に生成しておく
        self.position = pygame.Vector2(app_setting.screen_size.x, 0)

        self._score = 0
        self._hp = 0
        self._on_gained_score = None
        self._move_pattern = None
        self._shoot_pattern = None
        self.collider = box_collider.BoxCollider(self.position, self._size, self.on_intersected, CollisionLayer.Enemy)
        self._sound_destroy = pygame.mixer.Sound("resource/audio/se_main_enemy_destroyed.wav")
        self._boom_animation = AnimationObject(SpriteAnimation("resource/image/enemy_explode.png",
                                                               pygame.Vector2(32, 32), 0.5))

        self.disable()

    def setup(self, position, hp, size, score, move_pattern, shoot_pattern, on_gained_score, image_path):
        self.position = position
        self._hp = hp
        self._size.x = size
        self._size.y = size
        self._score = score
        self._move_pattern = move_pattern
        self._shoot_pattern = shoot_pattern
        self._on_gained_score = on_gained_score
        self._image = pygame.image.load(image_path)

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
        enemy_view_pos = self.position - self._size / 2
        screen.blit(self._image, enemy_view_pos)

    def on_intersected(self, collider):
        if collider.layer == CollisionLayer.PlayerShot:
            self._hp -= 1
            if self._hp <= 0:
                self._sound_destroy.play()
                self._on_gained_score(self._score)
                self._boom_animation.start(self.position)
                self.disable()

    def shoot(self, vec):
        instance = self._bullet_pool.rent()
        if instance is not None:
            instance.setup(pygame.Vector2(self.position), vec, self._bullet_size, self._bullet_pool)

    def disable(self):
        self.collider.enabled = False
        self.enabled = False
