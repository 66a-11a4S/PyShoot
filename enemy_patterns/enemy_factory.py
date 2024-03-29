import copy
from enemy_patterns.enemy_type import EnemyType
from enemy_patterns.interval_pattern import IntervalPattern
from enemy_patterns.move_patterns import *
from enemy_patterns.shoot_patterns import *
from game_objects.bullet import Bullet
from game_objects.enemy import Enemy
from object_pool import ObjectPool


class EnemyFactory:
    def __init__(self, player, on_gained_score):
        self._player = player
        self._on_gained_score = on_gained_score

        self._bullet_pool = ObjectPool(lambda: Bullet(is_player_bullet=False), init_size=256)
        self._enemy_pool = ObjectPool(lambda: Enemy(self._bullet_pool), init_size=64, max_size=128)
        self._status_table = {}
        self._move_patterns = {}
        self._shoot_patterns = {}

    def build_blueprint(self):
        def get_value(values, idx):
            if len(values) <= idx:
                return 0
            else:
                return float(values[idx])

        with open("resource/master_data/enemy_status.csv") as f:
            for enemy_type in EnemyType:
                line = f.readline()
                # 1つ目の Type はスキップ. csv も1行目はパラメータの説明なので読み飛ばす
                if enemy_type == EnemyType.Blank:
                    continue

                if len(line) == 0:
                    break

                parameter = line.rstrip().replace(' ', '').split(',')
                hp = get_value(parameter, 1)
                size = get_value(parameter, 2)
                score = get_value(parameter, 3)
                image_path = parameter[4]
                self._status_table[enemy_type.value] = (hp, size, score, image_path)

        with open("resource/master_data/enemy_move_pattern.csv") as f:
            for enemy_type in EnemyType:
                line = f.readline()
                # 1つ目の Type はスキップ. csv も1行目はパラメータの説明なので読み飛ばす
                if enemy_type == EnemyType.Blank:
                    continue

                if len(line) == 0:
                    break

                parameter = line.rstrip().replace(' ', '').split(',')
                move_type = parameter[1]
                speed = get_value(parameter, 2)
                wave_amp = get_value(parameter, 3)
                wave_duration = get_value(parameter, 4)
                stop_distance = get_value(parameter, 5)
                vertical_speed = get_value(parameter, 6)

                if move_type == "Horizontal":
                    move_pattern = horizontal_move.HorizontalMove(speed)
                elif move_type == "Wavy":
                    move_pattern = wavy.Wavy(speed, wave_amp, wave_duration)
                elif move_type == "Chase":
                    move_pattern = chase.Chase(speed, stop_distance)
                elif move_type == "VerticalChase":
                    move_pattern = vertical_chase.VerticalChase(speed, vertical_speed)

                self._move_patterns[enemy_type.value] = move_pattern

        with open("resource/master_data/enemy_shoot_pattern.csv") as f:
            for enemy_type in EnemyType:
                line = f.readline()
                # 1つ目の Type はスキップ. csv も1行目はパラメータの説明なので読み飛ばす
                if enemy_type == EnemyType.Blank:
                    continue

                if len(line) == 0:
                    break

                parameter = line.rstrip().replace(' ', '').split(',')
                shoot_type = parameter[1]
                interval = get_value(parameter, 2)
                speed = get_value(parameter, 3)
                ways = get_value(parameter, 4)
                angle = get_value(parameter, 5)

                if shoot_type == "Straight":
                    shoot_pattern = straight.Straight(speed, interval, ways, angle)
                elif shoot_type == "TargetCentric":
                    shoot_pattern = target_centric.TargetCentric(speed, interval, ways, angle)

                self._shoot_patterns[enemy_type.value] = shoot_pattern

    def create(self, position, enemy_type):
        hp = self._status_table[enemy_type][0]
        size = self._status_table[enemy_type][1]
        score = self._status_table[enemy_type][2]
        image_path = self._status_table[enemy_type][3]

        move = copy.deepcopy(self._move_patterns[enemy_type])
        move_pattern = IntervalPattern(move.interval, move.move)

        shoot = copy.deepcopy(self._shoot_patterns[enemy_type])
        shoot_pattern = IntervalPattern(shoot.interval, shoot.shoot)

        player_position = self._player.position
        move.setup(owner_position=position, target_position=player_position)
        shoot.setup(owner_position=position, target_position=player_position)
        instance = self._enemy_pool.rent()
        if instance is None:
            return None

        instance.setup(position, hp, size, score, move_pattern, shoot_pattern, self._on_gained_score, image_path)
        return instance
