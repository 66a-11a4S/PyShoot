from enum import auto, IntEnum


# 1チャンネルで1音だけ鳴らせるので、1音ずつ鳴らしたい種類を定義
class ChannelType(IntEnum):
    System = 0
    PlayerShot = auto()
    ReservedChannels = auto()
