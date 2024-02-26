import pygame
from enum import Enum
from scene.scene import Scene


class Title(Scene):
    class Menu(Enum):
        Start = 0,
        Exit = 1,
        Count = 2,

    def __init__(self):
        self._current_cursor = 0
        self._title_font = pygame.font.Font(None, 64)
        self._content_font = pygame.font.Font(None, 30)
        self._font_color = pygame.Color(255, 255, 255)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self._current_cursor = max(self._current_cursor - 1, 0)
        elif keys[pygame.K_s]:
            self._current_cursor = min(self._current_cursor + 1, Title.Menu.Count.value[0] - 1)

        if keys[pygame.K_SPACE]:
            self.execute_command(self._current_cursor)

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
            self.start_game()
        if cursor_pos == Title.Menu.Exit.value[0]:
            self.quit_game()

    def start_game(self):
        pass

    def quit_game(self):
        pass
