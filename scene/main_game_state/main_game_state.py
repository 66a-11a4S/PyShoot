class MainGameState:
    def __init__(self, on_changed_state):
        self._on_changed_state = on_changed_state

    def setup(self):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

    def invoke_next_stage(self, state_type):
        self._on_changed_state(state_type)
