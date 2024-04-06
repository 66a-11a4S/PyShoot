from collision.collider_pool import ColliderPool
from collision.collision_layer import CollisionLayer


class CollisionManager:
    def __init__(self):
        self._colliders = ColliderPool()
        self._collision_matrix = [
            [False, False, True, True],   # Player vs ...
            [False, False, True, False],  # PlayerShot vs ...
            [True, True, False, False],   # Enemy vs ...
            [True, False, False, False]   # EnemyShot vs ...
        ]

    def collision_check(self):
        self._colliders.update_all_layer()
        for layer_a in CollisionLayer:
            for layer_b in CollisionLayer:
                # 衝突をケアするレイヤーどうしで判定
                if not self._collision_matrix[layer_a.value][layer_b.value]:
                    continue

                layer_a_instances = self._colliders.get_instances(layer_a)
                layer_b_instances = self._colliders.get_instances(layer_b)
                self._collision_check_impl(layer_a_instances, layer_b_instances)

    def _collision_check_impl(self, colliders_a, colliders_b):
        for colA in colliders_a:
            for colB in colliders_b:
                if not self._need_collision_check(colA, colB):
                    continue

                if colA.intersected(colB):
                    colA.invoke_intersected(colB)
                    colB.invoke_intersected(colA)

    def _need_collision_check(self, col_a, col_b):
        if not col_a.enabled or not col_b.enabled:
            return False

        # 自己衝突は無効
        if col_a == col_b:
            return False

        return True
