import pygame
import app_setting
from enemy_patterns.enemy_type import EnemyType


class StageCoordinator:
    def __init__(self, enemy_factory, field):
        self._row_count = int(app_setting.screen_size.y // app_setting.tile_size)
        self._enemy_factory = enemy_factory
        self._before_spawn_column = 0
        self._field = field

    # 最初に画面内の敵を生成する
    def setup(self):
        tile_size = app_setting.tile_size
        column_count = int(app_setting.screen_size.x // tile_size)

        for x in range(column_count):
            for y in range(self._row_count):
                enemy_type = self._field.get_tile_value(x, y)
                if enemy_type == EnemyType.Blank.value[0]:
                    continue

                position = pygame.Vector2(x * tile_size, y * tile_size)
                self._enemy_factory.create(position, enemy_type)

    # stage を進行させ画面内部に入った敵を生成する
    def progress_stage(self):
        tile_size = app_setting.tile_size
        self._field.update()
        current_spawn_column = int(app_setting.screen_size.x + self._field.progress) // tile_size
        if self._before_spawn_column == 0:
            self._before_spawn_column = current_spawn_column

        # 右端の出現区画が変わった
        if current_spawn_column != self._before_spawn_column:
            # 右端の列を全て読み込み、敵が居れば生成する
            for y in range(self._row_count):
                enemy_type = self._field.get_tile_value(current_spawn_column, y)
                if enemy_type == EnemyType.Blank.value[0]:
                    continue

                position = pygame.Vector2(app_setting.screen_size.x, y * tile_size)
                self._enemy_factory.create(position, enemy_type)

        self._before_spawn_column = current_spawn_column
