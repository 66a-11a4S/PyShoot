import game_object


class Camera(game_object.GameObject):
    def __init__(self, upper_left, size):
        self.position = upper_left
        self.size = size
        self.scroll_speed = 32

    def update(self, dt):
        self.position.x += self.scroll_speed * dt

    def draw(self, screen, camera_position):
        pass
