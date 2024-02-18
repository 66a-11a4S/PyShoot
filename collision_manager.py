class CollisionManager:
    def __init__(self):
        self._colliders = []

    def setup(self, colliders):
        self._colliders = colliders

    def collision_check(self):
        for i in range(len(self._colliders)):
            for k in range(i, len(self._colliders)):
                if i == k:
                    continue

                colA = self._colliders[i]
                colB = self._colliders[k]
                # if !NeedCollisionCheck(colA, colB)
                #    continue;

                if colA.intersected(colB):
                    colA.invoke_intersected(colB)
                    colB.invoke_intersected(colA)
