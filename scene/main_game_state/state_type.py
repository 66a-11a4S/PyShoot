from enum import Enum


class StateType(Enum):
    Prepare = 0,
    Running = 1,
    GameOver = 2,
    GameClear = 3,
    End = 4,
