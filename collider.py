class Collider:
    def __init__(self, position, size, on_intersected):
        self._center = position
        self._size = size
        self.enabled = True
        self._on_intersected = on_intersected

    def sync_position(self, position):
        self._center = position

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
