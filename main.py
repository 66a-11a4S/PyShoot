import random

import pygame
import app_setting
from enemy_patterns.enemy_factory import EnemyFactory
from enemy_patterns.enemy_type import EnemyType
from game_objects import camera, player
from collision import collision_manager
from game_objects.game_object_manager import GameObjectManager

# pygame のセットアップ
pygame.init()
screen = pygame.display.set_mode(app_setting.screen_size)
clock = pygame.time.Clock()  # アプリケーションの時間進行を監視するオブジェクトを作成

# ゲーム内で動くオブジェクトを用意
camera = camera.Camera(pygame.Vector2(0, 0), app_setting.screen_size)
player = player.Player(pygame.Vector2(app_setting.screen_size / 2), camera.scroll_velocity, app_setting.screen_size)

enemy_factory = EnemyFactory(player)
enemies = []
for _ in range(30):
    x = random.randint(0, 320)
    y = random.randint(0, 240)
    enemy_type = random.randint(1, EnemyType.VerticalChase2.value[0])
    position = pygame.Vector2(320 + x, 120 + y)
    enemies.append(enemy_factory.create(position, enemy_type))

collision_manager = collision_manager.CollisionManager()

# 前フレームから何ミリ秒経過したか
dt = 0

manager = GameObjectManager()
running = True
while running:
    # event のポーリング
    for event in pygame.event.get():
        # pygame.QUIT: X を押してウィンドウを閉じられた
        if event.type == pygame.QUIT:
            running = False

    # 前のフレームの描画を塗りつぶして消す
    screen.fill(app_setting.bg_fill_color)

    manager.update()

    for go in manager.instances:
        if go.enabled:
            go.update(dt)

    collision_manager.collision_check()

    camera_pos = camera.position

    for go in manager.instances:
        if go.enabled:
            go.draw(screen, camera_pos)

    # スコアを表示する
    font = pygame.font.Font(None, 30)
    text = font.render(f'Score: {dt}', True, (255, 255, 255))
    screen.blit(text, pygame.Vector2(0, 0))

    # 描画内容を画面に反映する
    pygame.display.flip()

    # このメソッドを毎フレーム呼び出す. 引数を指定するとフレームレートの上限を設定できる.
    # 戻り値: 前回の呼び出しから何秒が経過したか
    dt = clock.tick(app_setting.frame_rate) / 1000

pygame.quit()
