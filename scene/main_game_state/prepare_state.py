import pygame
import app_setting
from scene.main_game_state.main_game_state import MainGameState
from scene.main_game_state.state_type import StateType


class PrepareState(MainGameState):
    def __init__(self, on_changed_state):
        super().__init__(on_changed_state)
        self._hud_font = pygame.font.Font(None, 30)
        self._hud_color = pygame.Color(255, 255, 255)
        self._prepare_duration = 3
        self._prepare_timer = 0.0

    def update(self, dt):
        self._prepare_timer += dt
        if self._prepare_duration <= self._prepare_timer:
            self.invoke_next_stage(StateType.Running)

    def draw(self, screen):
        text = self._hud_font.render('Are You Ready?', True, self._hud_color)
        screen_center = app_setting.screen_size * 0.5
        offset = pygame.Vector2(text.get_width() * 0.5, text.get_height() * 0.5)
        screen.blit(text, screen_center - offset)
