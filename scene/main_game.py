import pygame
import app_setting
from enum import Enum

from collision.collider_pool import ColliderPool
from collision.collision_manager import CollisionManager
from enemy_patterns.enemy_factory import EnemyFactory
from game_objects.camera import Camera
from game_objects.game_object_manager import GameObjectManager
from game_objects.player import Player
from scene.scene import Scene
from scene.scene_type import SceneType
from stage.stage_coordinator import StageCoordinator


class MainGame(Scene):
    class GameState(Enum):
        Prepare = 0,
        Running = 1,
        GameOver = 2,
        GameClear = 3,

    def __init__(self, change_scene_impl):
        super().__init__(change_scene_impl)

        # game sequence settings
        self._prepare_duration = 3

        # instance settings
        self._manager = GameObjectManager()
        self._collision_manager = CollisionManager()
        self._camera = Camera(pygame.Vector2(0, 0), app_setting.screen_size)
        self._player = Player(pygame.Vector2(app_setting.screen_size / 2), self._camera.scroll_velocity,
                              app_setting.screen_size)
        enemy_factory = EnemyFactory(self._player, self.on_gained_score)
        self._stage_coordinator = StageCoordinator(enemy_factory)

        # player settings
        self._player_rest = 3
        self._player.register_intersected(self.on_damaged)

        # HUD settings
        self.hud_font = pygame.font.Font(None, 30)
        self.hud_color = pygame.Color(255, 255, 255)

        # HUD elements
        self._prepare_timer = 0.0
        self._total_score = 0
        self._player_icon = pygame.image.load("resource/image/player.png")
        self._player_icon_width = self._player_icon.get_width()

        self._game_state = MainGame.GameState.Prepare

    def update(self, dt):
        if self._game_state is MainGame.GameState.Prepare:
            self.update_prepare(dt)
            return

        if self._game_state is MainGame.GameState.Running:
            self.update_running(dt)
            return

        if self._game_state is MainGame.GameState.GameOver:
            self.update_finished(dt)
            return

        if self._game_state is MainGame.GameState.GameClear:
            self.update_finished(dt)
            return

    def draw(self, screen, dt):
        self.draw_common_hud(screen, dt)

        if self._game_state is MainGame.GameState.Prepare:
            self.draw_prepare(screen)
            return

        if self._game_state is MainGame.GameState.Running:
            self.draw_running(screen)
            return

        if self._game_state is MainGame.GameState.GameOver:
            self.draw_game_over(screen)
            return

        if self._game_state is MainGame.GameState.GameClear:
            self.draw_game_clear(screen)
            return

    def dispose(self):
        self._manager.remove_all()
        ColliderPool().remove_all_layer()

    def update_prepare(self, dt):
        self._prepare_timer += dt
        self.update_game_objects(dt)
        if self._prepare_duration <= self._prepare_timer:
            self._game_state = MainGame.GameState.Running
            self._stage_coordinator.setup()

    def draw_prepare(self, screen):
        self.draw_game_objects(screen)
        text = self.hud_font.render('Are You Ready?', True, self.hud_color)
        screen_center = app_setting.screen_size * 0.5
        offset = pygame.Vector2(text.get_width() * 0.5, text.get_height() * 0.5)
        screen.blit(text, screen_center - offset)

    def update_running(self, dt):
        # ゲームを進行させる
        self._stage_coordinator.progress_stage()
        self.update_game_objects(dt)
        if self._stage_coordinator.has_end():
            self._game_state = MainGame.GameState.GameClear

    def draw_running(self, screen):
        self.draw_game_objects(screen)

    def draw_game_over(self, screen):
        self.draw_game_objects(screen)
        text = self.hud_font.render('Game Over', True, (255, 0, 0))
        screen_center = app_setting.screen_size * 0.5
        offset = pygame.Vector2(text.get_width() * 0.5, text.get_height() * 0.5)
        screen.blit(text, screen_center - offset)

    def draw_game_clear(self, screen):
        self.draw_game_objects(screen)
        text = self.hud_font.render('Game Clear', True, (0, 0, 255))
        screen_center = app_setting.screen_size * 0.5
        offset = pygame.Vector2(text.get_width() * 0.5, text.get_height() * 0.5)
        screen.blit(text, screen_center - offset)

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
            self._game_state = MainGame.GameState.GameOver
        else:
            self._player.start_recover()

    def on_gained_score(self, score):
        self._total_score += score

    def update_finished(self, _):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.change_scene(SceneType.Title)
