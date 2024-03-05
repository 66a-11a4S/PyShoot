import pygame

from game_objects.game_object import GameObject


# start すると表示されてアニメーションを再生し、再生し終えると非表示になるオブジェクト
class AnimationObject(GameObject):
    def __init__(self, animation):
        super().__init__()
        self._animation = animation

    def start(self):
        self.enabled = True
        self._animation.play()

    def update(self, dt):
        self._animation.update(dt)
        if self._animation.has_finished:
            self.enabled = False

    def draw(self, screen, dt):
        if self._animation.is_playing:
            screen.blit(self._animation.image, pygame.Vector2(0, 0), self._animation.surface_rect)
