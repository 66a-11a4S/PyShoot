from enum import IntEnum, auto


class CollisionLayer(IntEnum):
    Player = 0
    PlayerShot = auto()
    Enemy = auto()
    EnemyShot = auto()  # 末尾に ',' をつけないと tuple ではなく int とみなされる
