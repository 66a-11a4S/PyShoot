import pygame
from enum import Enum
from input.input_status import InputStatus
from scene.scene import Scene
from scene.scene_type import SceneType


class Title(Scene):
    class Menu(Enum):
        Start = 0,
        Exit = 1,
        Count = 2,

    def __init__(self, change_scene_impl):
        super().__init__(change_scene_impl)
        self._current_cursor = 0
        self._title_font = pygame.font.Font(None, 64)
        self._content_font = pygame.font.Font(None, 30)
        self._font_color = pygame.Color(255, 255, 255)
        self._sound_select = pygame.mixer.Sound("resource/audio/se_system_select.ogg")
        self._sound_decide = pygame.mixer.Sound("resource/audio/se_system_decide.ogg")

    def update(self, dt):
        prev_cursor = self._current_cursor
        if InputStatus().is_pressed(pygame.K_w):
            self._current_cursor = max(self._current_cursor - 1, 0)
        elif InputStatus().is_pressed(pygame.K_s):
            self._current_cursor = min(self._current_cursor + 1, Title.Menu.Count.value[0] - 1)

        if self._current_cursor is not prev_cursor:
            self._sound_select.play()

        if InputStatus().is_pressed(pygame.K_SPACE):
            self.execute_command(self._current_cursor)
            self._sound_decide.play()

    def draw(self, screen, dt):
        title_text = self._title_font.render('PyShoot', True, self._font_color)
        title_text_position = pygame.Vector2(240, 64)
        screen.blit(title_text, title_text_position)

        cursor_text = self._content_font.render('->', True, self._font_color)
        cursor_position = pygame.Vector2(256, 192) + self._current_cursor * pygame.Vector2(0, 64)
        screen.blit(cursor_text, cursor_position)

        for menu in Title.Menu:
            if menu == Title.Menu.Count:
                continue

            menu_text = self._content_font.render(menu.name, True, self._font_color)
            menu_position = pygame.Vector2(300, 192) + menu.value[0] * pygame.Vector2(0, 64)
            screen.blit(menu_text, menu_position)

    def execute_command(self, cursor_pos):
        if cursor_pos == Title.Menu.Start.value[0]:
            self.change_scene(SceneType.Main)
        if cursor_pos == Title.Menu.Exit.value[0]:
            self.change_scene(SceneType.Quit)
