import pygame

from enemy_patterns.enemy_type import EnemyType
from enemy_patterns.interval_pattern import IntervalPattern
from enemy_patterns.move_patterns import *
from enemy_patterns.shoot_patterns import *
from game_objects.bullet import Bullet
from game_objects.enemy import Enemy
from object_pool import ObjectPool


class EnemyFactory:
    def __init__(self, player):
        self._player = player
        self._bullet_pool = ObjectPool(lambda: Bullet(), init_size=256)
        self._enemy_pool = ObjectPool(lambda: Enemy(self._bullet_pool))

    def create(self, position, enemy_type):
        instance = self._enemy_pool.rent()
        interval = self.get_interval(enemy_type)
        player_position = self._player.position
        move_pattern = IntervalPattern(interval, self.create_move(position, enemy_type,
                                                                  interval, player_position).move)
        shoot_pattern = IntervalPattern(interval, self.create_shoot(position, enemy_type,
                                                                    interval, player_position).shoot)
        instance.setup(position, move_pattern, shoot_pattern)

    def get_interval(self, enemy_type):
        if enemy_type is EnemyType.Horizontal.value[0]:
            return 1
        if enemy_type is EnemyType.Horizontal2.value[0]:
            return 0.5
        if enemy_type is EnemyType.Wavy.value[0]:
            return 1
        if enemy_type is EnemyType.Wavy2.value[0]:
            return 0.5
        if enemy_type is EnemyType.Chase.value[0]:
            return 0.75
        if enemy_type is EnemyType.Chase2.value[0]:
            return 0.5
        if enemy_type is EnemyType.VerticalChase.value[0]:
            return 0.75
        if enemy_type is EnemyType.VerticalChase2.value[0]:
            return 0.5

        return 1

    def create_move(self, enemy_position, enemy_type, interval, player_position):
        if enemy_type is EnemyType.Horizontal.value[0]:
            return horizontal_move.HorizontalMove(speed=96)
        if enemy_type is EnemyType.Horizontal2.value[0]:
            return horizontal_move.HorizontalMove(speed=128)
        if enemy_type is EnemyType.Wavy.value[0]:
            return wavy.Wavy(horizontal_speed=96, amp=32, duration=interval)
        if enemy_type is EnemyType.Wavy2.value[0]:
            return wavy.Wavy(horizontal_speed=128, amp=64, duration=interval)
        if enemy_type is EnemyType.Chase.value[0]:
            return chase.Chase(owner_position=enemy_position, target_position=player_position,
                               speed=96, stop_distance=128)
        if enemy_type is EnemyType.Chase2.value[0]:
            return chase.Chase(owner_position=enemy_position, target_position=player_position,
                               speed=128, stop_distance=128)
        if enemy_type is EnemyType.VerticalChase.value[0]:
            return vertical_chase.VerticalChase(owner_position=enemy_position, target_position=player_position,
                                                velocity=pygame.Vector2(-192, 96))
        if enemy_type is EnemyType.VerticalChase2.value[0]:
            return vertical_chase.VerticalChase(owner_position=enemy_position, target_position=player_position,
                                                velocity=pygame.Vector2(-256, 96))
        return None

    def create_shoot(self, enemy_position, enemy_type, interval, player_position):
        if enemy_type is EnemyType.Horizontal.value[0]:
            return straight.Straight(interval, enemy_position, speed=128, ways=1, angle=0)
        if enemy_type is EnemyType.Horizontal2.value[0]:
            return straight.Straight(interval, enemy_position, speed=192, ways=3, angle=15)
        if enemy_type is EnemyType.Wavy.value[0]:
            return straight.Straight(interval, enemy_position, speed=128, ways=1, angle=0)
        if enemy_type is EnemyType.Wavy2.value[0]:
            return straight.Straight(interval, enemy_position, speed=192, ways=3, angle=15)
        if enemy_type is EnemyType.Chase.value[0]:
            return target_centric.TargetCentric(interval, enemy_position,
                                                target_position=player_position, speed=128, ways=1, angle=0)
        if enemy_type is EnemyType.Chase2.value[0]:
            return target_centric.TargetCentric(interval, enemy_position,
                                                target_position=player_position, speed=192, ways=3, angle=15)
        if enemy_type is EnemyType.VerticalChase.value[0]:
            return target_centric.TargetCentric(interval, enemy_position,
                                                target_position=player_position, speed=256, ways=1, angle=0)
        if enemy_type is EnemyType.VerticalChase2.value[0]:
            return target_centric.TargetCentric(interval, enemy_position,
                                                target_position=player_position, speed=312, ways=3, angle=15)
        return None
