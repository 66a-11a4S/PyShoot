from game_objects.game_object_manager import GameObjectManager


class GameObject:
    def __init__(self):
        self.enabled = True
        self._manager = GameObjectManager()
        self._manager.add(self)

    def update(self, dt):
        pass

    def draw(self, screen, camera_position):
        pass

    def dispose(self):
        self.enabled = False
        self._manager.remove(self)
