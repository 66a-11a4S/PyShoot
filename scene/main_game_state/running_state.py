from enemy_patterns.enemy_factory import EnemyFactory
from scene.main_game_state.main_game_state import MainGameState
from scene.main_game_state.state_type import StateType
from stage.stage_coordinator import StageCoordinator


class RunningState(MainGameState):
    def __init__(self, on_changed_state, on_gained_score, player):
        super().__init__(on_changed_state)

        enemy_factory = EnemyFactory(player, on_gained_score)
        self._stage_coordinator = StageCoordinator(enemy_factory)

    def setup(self):
        self._stage_coordinator.setup()

    def update(self, dt):
        self._stage_coordinator.progress_stage()
        if self._stage_coordinator.has_end():
            self.invoke_next_stage(StateType.GameClear)
