from collision import collider
import pygame


class SphereCollider(collider.Collider):
    def __init__(self, position, radius, on_intersected, layer):
        self._radius = radius
        size = pygame.Vector2(radius, radius)
        super().__init__(position, size, on_intersected, layer)

    def closest_position(self, position):
        # 中心から目標までのベクトルを出す
        vec = position - self.center
        # ベクトルの長さを円の半径でクランプ
        length = min(vec.length, self._radius)
        # 円の中心からベクトルの長さ分進んだ位置まで進める
        return self.center + vec.normalize * length

    # ダブルディスパッチ使うにも python ってオーバーロードできるのか? -> できない
    def intersected(self, coll):
        return coll.intersected_with_sphere(self)

    def intersected_with_sphere(self, sphere):
        vec = (sphere.center - self.center)
        return vec.length() <= (sphere._radius + self._radius)

    def intersected_with_rect(self, rect):
        closest_point_on_rect = rect.closest_position(self.center)
        vec = closest_point_on_rect - self.center
        return vec.length() <= self._radius

    def debug_draw(self, screen):
        pygame.draw.circle(screen, center=self.center, radius=self._radius, color=pygame.Color(128, 128, 255))
