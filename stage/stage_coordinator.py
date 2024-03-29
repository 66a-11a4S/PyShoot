import pygame
import app_setting
from enemy_patterns.enemy_type import EnemyType
from stage.field import Field


class StageCoordinator:
    def __init__(self, enemy_factory):
        self._row_count = int(app_setting.screen_size.y // app_setting.tile_size)
        self._enemy_factory = enemy_factory
        self._before_spawn_column = 0
        self._field = None
        self._enemy_factory.build_blueprint()
        self._spawned_enemies = []

    def setup(self):
        # with でスコープを抜けるとき自動で dispose 処理が走る
        # パスの位置は os.getcwd で確認できる
        tiles = []
        with open("resource/master_data/stage.csv") as f:
            for s in f.readlines():
                char_row = s.rstrip().replace(' ', '').split(',')
                # いわゆる collection 式. [ ] の中に collection を形成できる式を記述する
                tiles.append([int(c) for c in char_row])

        self._field = Field(tiles)

    # stage を進行させ画面内部に入った敵を生成する
    def progress_stage(self):
        tile_size = app_setting.tile_size
        self._field.update()
        current_spawn_column = int(app_setting.screen_size.x + self._field.progress) // tile_size
        if self._before_spawn_column <= 0:
            self._before_spawn_column = current_spawn_column
            return

        # 右端の出現区画が変わった
        if current_spawn_column != self._before_spawn_column:
            # 右端の列を全て読み込み、敵が居れば生成する
            for y in range(self._row_count):
                enemy_type = self._field.get_tile_value(current_spawn_column, y)
                if enemy_type == EnemyType.Blank.value:
                    continue

                position = pygame.Vector2(app_setting.screen_size.x, y * tile_size)
                instance = self._enemy_factory.create(position, enemy_type)
                if instance is not None:
                    self._spawned_enemies.append(instance)

        self._before_spawn_column = current_spawn_column

    # 敵が全滅 & ステージの端まで到達したら終了
    def has_end(self):
        for enemy in self._spawned_enemies:
            if enemy.enabled:
                return False

        return self._field.progress_is_max()
