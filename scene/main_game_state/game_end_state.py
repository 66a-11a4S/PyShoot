import pygame
import app_setting
from auido import audio_source
from auido.channel_id import ChannelType
from input.input_status import InputStatus
from scene.main_game_state.main_game_state import MainGameState
from scene.main_game_state.state_type import StateType


class GameEndState(MainGameState):
    def __init__(self, has_cleared, on_changed_state):
        super().__init__(on_changed_state)
        self._message = "Game Clear" if has_cleared else "Game Over"
        self._hud_font = pygame.font.Font(None, 30)
        self._hud_color = pygame.Color(0, 0, 255) if has_cleared else pygame.Color(255, 0, 0)
        self._jingle_channel = pygame.mixer.Channel(ChannelType.System.value)
        self._sound_jingle = audio_source.AudioSource("resource/audio/me_main_end.ogg")

    def setup(self):
        self._sound_jingle.play(channel=self._jingle_channel)

    def update(self, dt):
        if InputStatus().is_pressed(pygame.K_ESCAPE):
            self.invoke_next_stage(StateType.End)

    def draw(self, screen):
        text = self._hud_font.render(self._message, True, self._hud_color)
        screen_center = app_setting.screen_size * 0.5
        offset = pygame.Vector2(text.get_width() * 0.5, text.get_height() * 0.5)
        screen.blit(text, screen_center - offset)
