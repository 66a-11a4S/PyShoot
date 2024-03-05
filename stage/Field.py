import app_setting
from enemy_patterns.enemy_type import EnemyType


class Field:
    def __init__(self, tiles):
        self.progress = -app_setting.screen_size.x  # 1画面分、進行方向から反対側にスクロールした状態でスタート
        self._tiles = tiles
        self.col_count = len(self._tiles[0])
        self.row_count = app_setting.screen_size.y // app_setting.tile_size
        # 画面サイズからさらに右のマップ終端まで進む
        self._max_progress = max(0, len(tiles[0]) * app_setting.tile_size - app_setting.screen_size.x)

    def update(self):
        if self.progress < self._max_progress:
            self.progress += 1

    def progress_is_max(self):
        return self.progress == self._max_progress

    def get_tile_value(self, x, y):
        if x < 0 or self.col_count <= x:
            return EnemyType.Blank.value[0]
        if y < 0 or self.row_count <= y:
            return EnemyType.Blank.value[0]
        return self._tiles[y][x]
