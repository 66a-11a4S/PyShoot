from enum import Enum


# 1チャンネルで1音だけ鳴らせるので、1音ずつ鳴らしたい種類を定義
class ChannelType(Enum):
    System = 0,
    PlayerShot = 1,
    ReservedChannels = 2,
