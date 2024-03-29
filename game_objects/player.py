import pygame

from animation.animation_object import AnimationObject
from animation.sprite_animation import SpriteAnimation
from auido import audio_source
from auido.channel_id import ChannelType
from game_objects import game_object, bullet
from collision import sphere_collider
from collision.collision_layer import CollisionLayer
from input.input_status import InputStatus
from object_pool import ObjectPool


class Player(game_object.GameObject):
    _shoot_interval = 0.025
    _bullet_size = pygame.Vector2(6, 6)
    _bullet_velocity = pygame.Vector2(640, 0)
    _move_speed = 256
    _player_recover_time = 3
    _damaged_alpha = 128
    _boom_animation = AnimationObject(SpriteAnimation("resource/image/player_explode.png", pygame.Vector2(32, 32), 0.5))

    def __init__(self, position, screen_size):
        super().__init__()
        self.position = position
        self._shape = 16  # circle radius
        self._move_boundary = screen_size
        self.collider = sphere_collider.SphereCollider(self.position, self._shape, self.on_intersected,
                                                       CollisionLayer.Player)
        self._intersected_events = []
        self._intersected_events.append(self.damaged)

        self._bullet_pool = ObjectPool(lambda: bullet.Bullet(is_player_bullet=True), init_size=128)
        self._shoot_timer = 0.0

        self._recovering = False
        self._recover_timer = 0.0
        self._image = pygame.image.load("resource/image/player.png")

        # 自弾の連射音で他のチャンネルを埋めないようにする
        self._sound_shot_channel = pygame.mixer.Channel(ChannelType.PlayerShot.value)
        self._sound_shot = audio_source.AudioSource("resource/audio/se_main_player_shot.wav")
        self._sound_damage = audio_source.AudioSource("resource/audio/se_main_player_damage.ogg")

    def update(self, dt):
        self.update_position(dt)
        self.update_shoot(dt)

    def draw(self, screen, camera_position):
        player_view_position = self.position - pygame.Vector2(self._shape, self._shape)
        screen.blit(self._image, player_view_position)

    def on_intersected(self, _):
        for func in self._intersected_events:
            func()

    def update_position(self, dt):
        velocity = pygame.Vector2()

        if InputStatus().is_pressed(pygame.K_w):
            velocity.y = -1
        if InputStatus().is_pressed(pygame.K_s):
            velocity.y = 1
        if InputStatus().is_pressed(pygame.K_a):
            velocity.x = -1
        if InputStatus().is_pressed(pygame.K_d):
            velocity.x = 1

        if 0.01 < velocity.length():
            velocity = velocity.normalize() * self._move_speed * dt

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

        # 無敵復帰処理
        if self._recovering:
            self._recover_timer += dt
            if self._player_recover_time <= self._recover_timer:
                self._recovering = False
                self._recover_timer = 0
                self.collider.enabled = True
                self._image.set_alpha(255)

    def update_shoot(self, dt):
        if InputStatus().is_pressed(pygame.K_SPACE):
            if self._shoot_timer == 0.0:
                # 4-way shot
                self.shoot(self.position + pygame.Vector2(16, -8))
                self.shoot(self.position + pygame.Vector2(16, 8))
                self.shoot(self.position + pygame.Vector2(16, -16))
                self.shoot(self.position + pygame.Vector2(16, 16))
                self._sound_shot.play(channel=self._sound_shot_channel)

            self._shoot_timer += dt

            if self._shoot_interval < self._shoot_timer:
                self._shoot_timer = 0.0
        else:
            self._shoot_timer = 0.0

    def shoot(self, position):
        instance = self._bullet_pool.rent()
        if instance is not None:
            instance.setup(pygame.Vector2(position), self._bullet_velocity, self._bullet_size, self._bullet_pool)

    def damaged(self):
        self.enabled = False
        self.collider.enabled = False
        self._image.set_alpha(self._damaged_alpha)
        self._sound_damage.play()
        self._boom_animation.start(self.position)

    def start_recover(self):
        self.enabled = True
        self._recovering = True

    def register_intersected(self, func):
        self._intersected_events.append(func)
