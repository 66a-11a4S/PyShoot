from instance_manager import InstanceManager


class ColliderPool:
    # singleton instance
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ColliderPool, cls).__new__(cls)
            cls._instance_manager = InstanceManager()
        return cls._instance

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

