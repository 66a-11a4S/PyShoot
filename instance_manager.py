class InstanceManager:
    def __init__(self):
        self.actual_instance = []
        self.add_requested = []
        self.remove_requested = []

    # @property 属性をつけると getter としてみなされ、関数呼び出しの () をつけずに値を参照できる
    @property
    def instances(self):
        return self.actual_instance + self.add_requested

    def add(self, instance):
        self.add_requested.append(instance)

    def remove(self, instance):
        self.remove_requested.append(instance)

    def remove_all(self):
        self.actual_instance.clear()

    def update(self):
        # TODO: Remove が O(n) なので呼び出し頻度次第で代替案を検討
        for instance in self.remove_requested:
            self.actual_instance.remove(instance)

        self.remove_requested.clear()

        for instance in self.add_requested:
            self.actual_instance.append(instance)

        self.add_requested.clear()
