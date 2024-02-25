import pygame
from enemy_patterns.move_patterns.move_pattern import MovePattern


# 自機を追いかける
class Chase(MovePattern):
    def __init__(self, speed, stop_distance):
        super().__init__()
        self._speed = speed
        self.stop_distance = stop_distance

    def move(self, _):
        vec = self._target_position - self._owner_position
        length = vec.length()
        # 停止位置を通り越して止まりそうなら、停止位置までの移動速度に丸める
        if length < self.stop_distance:
            return pygame.Vector2(0, 0)

        return vec.normalize() * self._speed
