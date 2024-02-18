class CollisionManager:
    def __init__(self):
        self._colliders = []
        self._collision_matrix = [
            [False, False, True, True],   # Player vs ...
            [False, False, True, False],  # PlayerShot vs ...
            [True, True, False, False],   # Enemy vs ...
            [True, False, False, False]   # EnemyShot vs ...
        ]

    def setup(self, colliders):
        self._colliders = colliders

    def collision_check(self):
        for i in range(len(self._colliders)):
            for k in range(i, len(self._colliders)):
                if i == k:
                    continue

                colA = self._colliders[i]
                colB = self._colliders[k]

                if not self.need_collision_check(colA, colB):
                    continue

                if colA.intersected(colB):
                    colA.invoke_intersected(colB)
                    colB.invoke_intersected(colA)

    def need_collision_check(self, col_a, col_b):
        if not col_a.enabled or not col_b.enabled:
            return False

        if not self._collision_matrix[col_a.layer.value[0]][col_b.layer.value[0]]:
            return False

        return True
