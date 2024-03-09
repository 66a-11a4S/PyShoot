from enum import Enum, auto


class StateType(Enum):
    Prepare = auto(),
    Running = auto(),
    GameOver = auto(),
    GameClear = auto(),
    End = auto(),
