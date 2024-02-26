from scene.Title import Title
from scene.main_game import MainGame
from scene.scene_type import SceneType


class SceneRunner:
    def __init__(self):
        self._current_scene = None

    def run(self, screen, dt):
        self._current_scene.update(dt)
        self._current_scene.draw(screen, dt)

    def change_scene(self, scene_type):
        if self._current_scene is not None:
            self._current_scene.dispose()
            self._current_scene = None

        if scene_type is not SceneType.Blank:
            self._current_scene = self.create_scene(scene_type)
            self._current_scene.setup()

    def create_scene(self, scene_type):
        if scene_type == SceneType.Title:
            return Title()
        if scene_type == SceneType.Main:
            return MainGame()

        return None
