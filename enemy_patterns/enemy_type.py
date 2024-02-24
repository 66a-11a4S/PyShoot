from enum import Enum


class EnemyType(Enum):
    Horizontal = 0,  # 横一直線 + 正面
    Horizontal2 = 1,  # 横一直線 + 3way
    Wavy = 2,  # 波形 + 正面
    Wavy2 = 3,  # 横一直線 + 3way
    Chase = 4,  # 横一直線 + 自機狙い
    Chase2 = 5,  # 横一直線 + 自機狙い3way
    VerticalChase = 6,  # 縦軸合わせ + 自機狙い
    VerticalChase2 = 7,  # 縦軸合わせ + 自機外し2way
