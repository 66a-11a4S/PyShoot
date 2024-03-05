import pygame
import app_setting

from collision.collider_pool import ColliderPool
from collision.collision_manager import CollisionManager
from game_objects.camera import Camera
from game_objects.game_object_manager import GameObjectManager
from game_objects.player import Player
from scene.main_game_state.game_end_state import GameEndState
from scene.main_game_state.prepare_state import PrepareState
from scene.main_game_state.running_state import RunningState
from scene.main_game_state.state_type import StateType
from scene.scene import Scene
from scene.scene_type import SceneType


class MainGame(Scene):
    def __init__(self, change_scene_impl):
        super().__init__(change_scene_impl)

        # instance settings
        self._manager = GameObjectManager()
        self._collision_manager = CollisionManager()
        self._camera = Camera(pygame.Vector2(0, 0))
        self._player = Player(pygame.Vector2(app_setting.screen_size / 2), app_setting.screen_size)

        # player settings
        self._player_rest = 3
        self._player.register_intersected(self.on_damaged)

        # HUD settings
        self.hud_font = pygame.font.Font(None, 30)
        self.hud_color = pygame.Color(255, 255, 255)

        # HUD elements
        self._total_score = 0
        self._player_icon = pygame.image.load("resource/image/player.png")
        self._player_icon_width = self._player_icon.get_width()

        # audio
        pygame.mixer_music.load("resource/audio/bgm_main.mp3")

        self._game_state = None
        self.on_changed_state(StateType.Prepare)

    def update(self, dt):
        self._game_state.update(dt)
        if type(self._game_state) is not GameEndState:
            self.update_game_objects(dt)

    def draw(self, screen, dt):
        self.draw_common_hud(screen, dt)
        self._game_state.draw(screen)
        self.draw_game_objects(screen)

    def dispose(self):
        self._manager.remove_all()
        ColliderPool().remove_all_layer()
        pygame.mixer_music.stop()

    def update_game_objects(self, dt):
        self._manager.update()
        for go in self._manager.instances:
            if go.enabled:
                go.update(dt)

        self._collision_manager.collision_check()

    def draw_game_objects(self, screen):
        camera_pos = self._camera.position
        for go in self._manager.instances:
            if go.enabled:
                go.draw(screen, camera_pos)

    def draw_common_hud(self, screen, dt):
        fps_text = self.hud_font.render(f'tick: {dt}', True, self.hud_color)
        screen.blit(fps_text, pygame.Vector2(app_setting.screen_size.x - 128, 0))
        text = self.hud_font.render(f'Score: {self._total_score}', True, self.hud_color)
        screen.blit(text, pygame.Vector2(192, 0))
        text = self.hud_font.render(f'Player: ', True, self.hud_color)
        screen.blit(text, pygame.Vector2(0, 0))
        for x in range(self._player_rest):
            screen.blit(self._player_icon, pygame.Vector2(80 + x * (self._player_icon_width + 4), 0))

    def on_damaged(self):
        self._player_rest -= 1
        if self._player_rest == 0:
            self.on_changed_state(StateType.GameOver)
        else:
            self._player.start_recover()

    def on_gained_score(self, score):
        self._total_score += score

    def on_changed_state(self, state):
        next_state = self.create_state(state)
        if next_state is None:
            self.change_scene(SceneType.Title)
            return

        next_state.setup()
        self._game_state = next_state
        self.manage_bgm(state)

    def create_state(self, state):
        if state is StateType.Prepare:
            return PrepareState(self.on_changed_state)
        elif state is StateType.Running:
            return RunningState(self.on_changed_state, self.on_gained_score, self._player)
        elif state is StateType.GameOver:
            return GameEndState(False, self.on_changed_state)
        elif state is StateType.GameClear:
            return GameEndState(True, self.on_changed_state)

    def manage_bgm(self, state):
        if state is StateType.Running:
            return

        if state is StateType.Prepare:
            pygame.mixer_music.play()
            return
        else:
            pygame.mixer_music.stop()
