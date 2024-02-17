import random
import pygame
import game_object


class Enemy(game_object.GameObject):
    def __init__(self):
        self.position = pygame.Vector2(random.randint(0, 640), random.randint(0, 480))
        self.shape = pygame.Rect(self.position, pygame.Vector2(32, 32))
        self.material = pygame.Color(255, 128, 128)

    def update(self, dt):
        pass

    def draw(self, screen, camera_position):
        enemy_view_pos = self.position - camera_position
        self.shape.x = enemy_view_pos.x
        self.shape.y = enemy_view_pos.y
        pygame.draw.rect(screen, self.material, self.shape)
