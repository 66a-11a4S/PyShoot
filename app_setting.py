import pygame


frame_rate = 60
screen_size = pygame.Vector2(640, 480)
bg_fill_color = pygame.Color(0, 0, 64)
tile_size = 32


def is_in_screen(position, margin=pygame.Vector2()):
    if position.x < -margin.x:
        return False
    if position.y < -margin.y:
        return False
    if screen_size.x + margin.x < position.x:
        return False
    if screen_size.y + margin.y < position.y:
        return False
    return True
