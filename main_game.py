import pygame
from enum import Enum
from collision.collision_manager import CollisionManager
from game_objects.game_object_manager import GameObjectManager
from stage.stage_coordinator import StageCoordinator


class MainGame:
    class GameState(Enum):
        Prepare = 0,
        Running = 1,
        GameOver = 2

    def __init__(self, player, camera):
        # game sequence settings
        self._prepare_duration = 3

        # instance settings
        self._manager = GameObjectManager()
        self._collision_manager = CollisionManager()
        self._player = player
        self._camera = camera
        self._stage_coordinator = StageCoordinator(self._player)

        # player settings
        self._player_rest = 3
        self._player.register_intersected(self.on_damaged)

        self._prepare_timer = 0.0
        self._game_state = MainGame.GameState.Prepare

    def update(self, screen, dt):
        if self._game_state is MainGame.GameState.Prepare:
            self.update_prepare(dt)
            self.draw_prepare(screen)
            return

        if self._game_state is MainGame.GameState.Running:
            self.update_running(dt)
            self.draw_running(screen, dt)
            return

        if self._game_state is MainGame.GameState.GameOver:
            self.draw_game_over(screen)
            return

    def update_prepare(self, dt):
        self._prepare_timer += dt
        self.update_game_objects(dt)
        if self._prepare_duration <= self._prepare_timer:
            self._game_state = MainGame.GameState.Running
            self._stage_coordinator.setup()

    def draw_prepare(self, screen):
        self.draw_game_objects(screen)
        font = pygame.font.Font(None, 30)
        text = font.render('Are You Ready?', True, (255, 255, 255))
        screen.blit(text, pygame.Vector2(0, 0))

    def update_running(self, dt):
        # ゲームを進行させる
        self._stage_coordinator.progress_stage()
        self.update_game_objects(dt)

    def draw_running(self, screen, dt):
        self.draw_game_objects(screen)
        font = pygame.font.Font(None, 30)
        text = font.render(f'Score: {dt}', True, (255, 255, 255))
        screen.blit(text, pygame.Vector2(0, 0))

    def draw_game_over(self, screen):
        self.draw_game_objects(screen)
        font = pygame.font.Font(None, 30)
        text = font.render('GameOver', True, (255, 255, 255))
        screen.blit(text, pygame.Vector2(0, 0))
        pass

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

    def on_damaged(self):
        self._player_rest -= 1
        if self._player_rest == 0:
            self._game_state = MainGame.GameState.GameOver
        else:
            self._player.start_recover()
