from scene.Title import Title
from scene.main_game import MainGame
from scene.scene_type import SceneType


class SceneRunner:
    def __init__(self):
        self._current_scene = None
        self._running = False
        self._change_scene_request = None

    @property
    def is_running(self):
        return self._running

    def start(self):
        self._running = True

    def run(self, screen, dt):
        if self._change_scene_request is not None:
            self.change_scene_impl(self._change_scene_request)
            self._change_scene_request = None

        if self._current_scene is None:
            return

        self._current_scene.update(dt)
        self._current_scene.draw(screen, dt)

    def request_change_scene(self, scene_type):
        self._change_scene_request = scene_type

    def change_scene_impl(self, scene_type):
        if self._current_scene is not None:
            self._current_scene.dispose()
            self._current_scene = None

        if scene_type is SceneType.Quit:
            self._running = False
            return

        if scene_type is not SceneType.Blank:
            self._current_scene = self.create_scene(scene_type)
            self._current_scene.setup()

    def create_scene(self, scene_type):
        if scene_type == SceneType.Title:
            return Title(self.request_change_scene)
        if scene_type == SceneType.Main:
            return MainGame(self.request_change_scene)

        return None
