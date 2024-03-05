class InstanceManager:
    def __init__(self):
        self._actual_instance = []
        self._add_requested = []
        self._remove_requested = []

    # @property 属性をつけると getter としてみなされ、関数呼び出しの () をつけずに値を参照できる
    @property
    def instances(self):
        return self._actual_instance + self._add_requested

    def add(self, instance):
        self._add_requested.append(instance)

    def remove(self, instance):
        self._remove_requested.append(instance)

    def remove_all(self):
        self._remove_requested.clear()
        self._actual_instance.clear()
        self._add_requested.clear()

    def update(self):
        # TODO: Remove が O(n) なので呼び出し頻度次第で代替案を検討
        for instance in self._remove_requested:
            self._actual_instance.remove(instance)

        self._remove_requested.clear()

        for instance in self._add_requested:
            self._actual_instance.append(instance)

        self._add_requested.clear()
