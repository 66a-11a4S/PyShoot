from collision import collider
import pygame


class BoxCollider(collider.Collider):
    def __init__(self, position, size, on_intersected, layer):
        super().__init__(position, size, on_intersected, layer)

    def closest_position(self, position):
        self_min = self.get_min()
        self_max = self.get_max()

        x = min(self_max.x, max(position.x, self_min.x))
        y = min(self_max.y, max(position.y, self_min.y))
        return pygame.Vector2(x, y)

    def intersected(self, coll):
        return coll.intersected_with_rect(self)

    def intersected_with_sphere(self, sphere):
        return sphere.intersected_with_rect(self)

    def intersected_with_rect(self, rect):
        self_min = self.get_min()
        self_max = self.get_max()
        rect_min = rect.get_min()
        rect_max = rect.get_max()

        return rect_min.x < self_max.x and\
            rect_max.x > self_min.x and\
            rect_min.y < self_max.y and\
            rect_max.y > self_min.y

    def debug_draw(self, screen):
        min_pos = self.get_min()
        max_pos = self.get_max()
        debug_rect = pygame.Rect(left=min_pos.x, top=max_pos.y, width=self.size.x, height=self.size.y)
        pygame.draw.rect(screen, pygame.Color(255, 128, 128), debug_rect)

    def get_min(self):
        return self.center - self.size / 2

    def get_max(self):
        return self.center + self.size / 2
