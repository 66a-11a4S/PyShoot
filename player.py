import pygame
import game_object


class Player(game_object.GameObject):
    def __init__(self, position, scroll_velocity):
        self.position = position
        self.material = pygame.Color(128, 128, 255)
        self.shape = 32  # circle radius
        self.move_speed = 256
        self.scroll_velocity = scroll_velocity

    def update(self, dt):
        velocity = self.scroll_velocity * dt

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            velocity.y -= self.move_speed * dt
        if keys[pygame.K_s]:
            velocity.y += self.move_speed * dt
        if keys[pygame.K_a]:
            velocity.x -= self.move_speed * dt
        if keys[pygame.K_d]:
            velocity.x += self.move_speed * dt

        self.position += velocity

    def draw(self, screen, camera_position):
        player_view_position = self.position - camera_position
        pygame.draw.circle(screen, self.material, player_view_position, self.shape)

