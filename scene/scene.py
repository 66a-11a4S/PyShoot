class Scene:
    def __init__(self, change_scene_impl):
        self._change_scene_impl = change_scene_impl

    def change_scene(self, scene_type):
        self._change_scene_impl(scene_type)

    def setup(self):
        pass

    def update(self, dt):
        pass

    def draw(self, screen, dt):
        pass

    def dispose(self):
        pass
