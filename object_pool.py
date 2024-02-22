from collections import deque


class ObjectPool:
    def __init__(self, instance_factory, init_size=16):
        # list だと append は O(1) だが remove は O(n) なので、追加と削除が両方O(1)の queue を使う
        self.not_used = deque()
        self.instance_factory = instance_factory
        self.current_size = 0
        for _ in range(init_size):
            instance = self.instance_factory()
            self.not_used.append(instance)
            self.current_size += 1

    def rent(self):
        if len(self.not_used) == 0:
            self.extends()

        instance = self.not_used.pop()
        return instance

    def back(self, instance):
        self.not_used.append(instance)

    def extends(self):
        current_size = self.current_size
        # 長さを二倍にする
        for _ in range(current_size):
            instance = self.instance_factory()
            self.not_used.append(instance)
            self.current_size += 1

        print(f"pool extended: {self.current_size}")
