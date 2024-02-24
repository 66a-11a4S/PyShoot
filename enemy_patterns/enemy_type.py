from enum import Enum


class EnemyType(Enum):
    Blank = 0
    Horizontal = 1,  # 横一直線 + 正面
    Horizontal2 = 2,  # 横一直線 + 3way
    Wavy = 3,  # 波形 + 正面
    Wavy2 = 4,  # 横一直線 + 3way
    Chase = 5,  # 横一直線 + 自機狙い
    Chase2 = 6,  # 横一直線 + 自機狙い3way
    VerticalChase = 7,  # 縦軸合わせ + 自機狙い
    VerticalChase2 = 8,  # 縦軸合わせ + 自機外し2way
