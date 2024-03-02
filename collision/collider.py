from collision.collider_pool import ColliderPool


class Collider:
    def __init__(self, position, size, on_intersected, layer):
        self.center = position
        self.size = size
        self._on_intersected = on_intersected
        self.enabled = True
        self._manager = ColliderPool()
        self._manager.add(self)
        self._layer = layer
        self._layer_value = layer.value[0]

    @property
    def layer_value(self):
        return self._layer_value

    def set_layer(self, layer):
        self._layer = layer
        self._layer_value = layer.value[0]

    def sync_position(self, position):
        self.center = position

    def invoke_intersected(self, coll):
        self._on_intersected(coll)
        pass

    def closest_position(self, position):
        pass

    def intersected(self, coll):
        pass

    def intersected_with_sphere(self, coll):
        pass

    def intersected_with_rect(self, coll):
        pass

    def debug_draw(self, screen):
        pass

    def dispose(self):
        self._manager.remove(self)