from enum import Enum
import pygame


class MainGame:
    class GameState(Enum):
        Prepare = 0,
        Running = 1,
        GameOver = 2

    def __init__(self, player):
        # game sequence settings
        self._prepare_duration = 3

        # player settings
        self._player_rest = 3
        self._player = player
        self._player.register_intersected(self.on_damaged)

        self._prepare_timer = 0.0
        self._game_state = MainGame.GameState.Prepare

    def update(self, screen, dt):
        if self._game_state is MainGame.GameState.Prepare:
            self.update_prepare(screen, dt)
            return
        if self._game_state is MainGame.GameState.Running:
            self.update_running(screen, dt)
            return
        if self._game_state is MainGame.GameState.GameOver:
            self.update_game_over(screen, dt)
            return

    def update_prepare(self, screen, dt):
        self._prepare_timer += dt
        if self._prepare_duration <= self._prepare_timer:
            self._game_state = MainGame.GameState.Running
            return

        font = pygame.font.Font(None, 30)
        text = font.render('Are You Ready?', True, (255, 255, 255))
        screen.blit(text, pygame.Vector2(0, 0))
        pass

    def update_running(self, screen, dt):
        font = pygame.font.Font(None, 30)
        text = font.render(f'Score: {dt}', True, (255, 255, 255))
        screen.blit(text, pygame.Vector2(0, 0))

    def update_game_over(self, screen, dt):
        font = pygame.font.Font(None, 30)
        text = font.render('GameOver', True, (255, 255, 255))
        screen.blit(text, pygame.Vector2(0, 0))
        pass

    def on_damaged(self):
        self._player_rest -= 1
        if self._player_rest == 0:
            self._game_state = MainGame.GameState.GameOver
        else:
            self._player.start_recover()
