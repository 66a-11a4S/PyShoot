import pygame


frame_rate = 60
screen_size = pygame.Vector2(640, 480)
bg_fill_color = pygame.Color(128, 128, 128)


def is_in_screen(position):
    if position.x < 0:
        return False
    if position.y < 0:
        return False
    if screen_size.x < position.x:
        return False
    if screen_size.y < position.y:
        return False
    return True
