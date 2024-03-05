# 一定時間毎に func を実行する
class IntervalPattern:
    def __init__(self, interval, func):
        self._interval = interval
        self._timer = 0.0
        self._func = func

    def update(self, dt):
        self._timer += dt
        clamped_timer = min(self._timer, self._interval)
        self._timer %= self._interval
        return self._func(clamped_timer)

    def reset(self):
        self._timer = 0.0

    @property
    def duration(self):
        return self._interval
