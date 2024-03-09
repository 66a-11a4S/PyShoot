from enum import IntEnum, auto


class EnemyType(IntEnum):
    Blank = 0
    Horizontal = auto()  # 横一直線 + 正面
    Horizontal2 = auto()  # 横一直線 + 3way
    Wavy = auto()  # 波形 + 正面
    Wavy2 = auto()  # 横一直線 + 3way
    Chase = auto()  # 横一直線 + 自機狙い
    Chase2 = auto()  # 横一直線 + 自機狙い3way
    VerticalChase = auto()  # 縦軸合わせ + 自機狙い
    VerticalChase2 = auto()  # 縦軸合わせ + 自機外し2way
    Count = auto()
