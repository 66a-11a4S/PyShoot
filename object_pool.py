from collections import deque


class ObjectPool:
    # プールサイズのデフォルト値は本PJにおける一般的な利用シーンを想定.
    # bullet など必要数が多くなりそうな場面で明示的に設定する.
    def __init__(self, instance_factory, init_size=16, max_size=64):
        # list だと append は O(1) だが remove は O(n) なので、追加と削除が両方O(1)の queue を使う
        self.not_used = deque()
        self.instance_factory = instance_factory
        self.current_size = 0
        self._max_size = max_size
        for _ in range(min(max_size, init_size)):
            instance = self.instance_factory()
            self.not_used.append(instance)
            self.current_size += 1

    def rent(self):
        if len(self.not_used) == 0:
            self.extends()

        if len(self.not_used) == 0:
            return None

        instance = self.not_used.pop()
        return instance

    def back(self, instance):
        self.not_used.append(instance)

    def extends(self):
        current_size = self.current_size
        rest_of_increase = self._max_size - current_size
        increase_length = min(current_size, rest_of_increase)  # 長さを二倍にする
        if increase_length == 0:
            return

        for _ in range(increase_length):
            instance = self.instance_factory()
            self.not_used.append(instance)
            self.current_size += 1

        # print(f"pool extended: {self.current_size}")
