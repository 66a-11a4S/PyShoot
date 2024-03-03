from collision.collision_layer import CollisionLayer
from instance_manager import InstanceManager


class ColliderPool:
    # singleton instance
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ColliderPool, cls).__new__(cls)
            cls._instance_manager = InstanceManager()

            # __new__ メソッド内部では insert ができない
            cls._instance_manager_table = \
                {
                    CollisionLayer.Player: InstanceManager(),
                    CollisionLayer.PlayerShot: InstanceManager(),
                    CollisionLayer.Enemy: InstanceManager(),
                    CollisionLayer.EnemyShot: InstanceManager(),
                }

        return cls._instance

    def __init__(self):
        for layer in CollisionLayer:
            self._instance_manager_table[layer] = InstanceManager()

    def get_instances(self, layer):
        return self._instance_manager_table[layer].instances

    def add(self, instance, layer):
        return self._instance_manager_table[layer].add(instance)

    def remove(self, instance, layer):
        self._instance_manager_table[layer].remove(instance)

    def remove_all(self, layer):
        self._instance_manager_table[layer].remove_all()

    def remove_all_layer(self):
        for layer in CollisionLayer:
            self.remove_all(layer)

    def update(self, layer):
        self._instance_manager_table[layer].update()

    def update_all_layer(self):
        for layer in CollisionLayer:
            self.update(layer)
