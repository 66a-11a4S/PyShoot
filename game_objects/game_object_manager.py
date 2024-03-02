from instance_manager import InstanceManager


class GameObjectManager:
    # singleton instance
    _instance = None

    def __new__(cls):
        # __new__  や __init__ はクラスを生成しようとするたびに毎回呼ばれる
        if cls._instance is None:
            cls._instance = super(GameObjectManager, cls).__new__(cls)
            cls._instance_manager = InstanceManager()
        return cls._instance

    # @property 属性をつけると getter としてみなされ、関数呼び出しの () をつけずに値を参照できる
    @property
    def instances(self):
        return self._instance_manager.instances

    def add(self, instance):
        self._instance_manager.add(instance)

    def remove(self, instance):
        self._instance_manager.remove(instance)

    def remove_all(self):
        self._instance_manager.remove_all()

    def update(self):
        self._instance_manager.update()
