from enum import Enum


class CollisionLayer(Enum):
    Player = 0,
    PlayerShot = 1,
    Enemy = 2,
    EnemyShot = 3,  # 末尾に ',' をつけないと tuple ではなく int とみなされる
