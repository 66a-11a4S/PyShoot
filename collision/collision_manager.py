from collision.collider_pool import ColliderPool


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
        self._colliders.update()
        colliders = self._colliders.instances
        for i in range(len(colliders)):
            for k in range(i, len(colliders)):
                if i == k:
                    continue

                colA = colliders[i]
                colB = colliders[k]

                if not self.need_collision_check(colA, colB):
                    continue

                if colA.intersected(colB):
                    colA.invoke_intersected(colB)
                    colB.invoke_intersected(colA)

    def need_collision_check(self, col_a, col_b):
        if not col_a.enabled or not col_b.enabled:
            return False

        # col_a.layer.value[0] にアクセスする部分で bottle-neck になっていたのでキャッシュされた value を参照する.
        # python の Enum はクラスだからか?
        if not self._collision_matrix[col_a.layer_value][col_b.layer_value]:
            return False

        return True
