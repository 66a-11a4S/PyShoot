import pygame
import game_object


class Player(game_object.GameObject):
    def __init__(self, position):
        self.position = position
        self.material = pygame.Color(128, 128, 255)
        self.shape = 32  # circle radius
        self.move_speed = 256

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.position.y -= self.move_speed * dt
        if keys[pygame.K_s]:
            self.position.y += self.move_speed * dt
        if keys[pygame.K_a]:
            self.position.x -= self.move_speed * dt
        if keys[pygame.K_d]:
            self.position.x += self.move_speed * dt

    def draw(self, screen, camera_position):
        player_view_position = self.position - camera_position
        pygame.draw.circle(screen, self.material, player_view_position, self.shape)

