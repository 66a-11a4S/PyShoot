class GameObjectManager:
    # singleton instance
    _instance = None

    def __new__(cls):
        # __new__  や __init__ はクラスを生成しようとするたびに毎回呼ばれる
        if cls._instance is None:
            cls._instance = super(GameObjectManager, cls).__new__(cls)
            cls.actual_instance = []
            cls.add_requested = []
            cls.remove_requested = []
        return cls._instance

    # @property 属性をつけると getter としてみなされ、関数呼び出しの () をつけずに値を参照できる
    @property
    def instances(self):
        return self.actual_instance + self.add_requested

    def add(self, instance):
        self.add_requested.append(instance)

    def remove(self, instance):
        self.remove_requested.append(instance)

    def update(self):
        # TODO: Remove が O(n) なので呼び出し頻度次第で代替案を検討
        for instance in self.remove_requested:
            self.actual_instance.remove(instance)

        self.remove_requested.clear()

        for instance in self.add_requested:
            self.actual_instance.append(instance)

        self.add_requested.clear()
