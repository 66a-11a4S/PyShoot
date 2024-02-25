import pygame
import app_setting
from enemy_patterns.enemy_factory import EnemyFactory
from enemy_patterns.enemy_type import EnemyType
from stage.Field import Field


class StageCoordinator:
    def __init__(self, player):
        self._row_count = int(app_setting.screen_size.y // app_setting.tile_size)
        self._enemy_factory = EnemyFactory(player)
        self._before_spawn_column = 0
        self._field = None
        self._enemy_factory.build_blueprint()

    # 最初に画面内の敵を生成する
    def setup(self):
        tile_size = app_setting.tile_size
        column_count = int(app_setting.screen_size.x // tile_size)

        # with でスコープを抜けるとき自動で dispose 処理が走る
        # パスの位置は os.getcwd で確認できる
        tiles = []
        with open("resource/stage.csv") as f:
            for s in f.readlines():
                char_row = s.rstrip().replace(' ', '').split(',')
                # いわゆる collection 式. [ ] の中に collection を形成できる式を記述する
                tiles.append([int(c) for c in char_row])

        self._field = Field(tiles)
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
