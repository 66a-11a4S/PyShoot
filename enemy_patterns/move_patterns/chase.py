# 自機を追いかける
import pygame


class Chase:
    def __init__(self, owner_position, target_position, speed, stop_distance):
        self._owner_position = owner_position
        self._target_position = target_position
        self._speed = speed
        self.stop_distance = stop_distance

    def move(self, _):
        vec = self._target_position - self._owner_position
        length = vec.length()
        # 停止位置を通り越して止まりそうなら、停止位置までの移動速度に丸める
        if length < self.stop_distance:
            return pygame.Vector2(0, 0)

        print(self._owner_position)
        return vec.normalize() * self._speed
