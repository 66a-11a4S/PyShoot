import pygame
import player
import enemy
import camera
import app_setting
import collision_manager


app = app_setting.AppSetting()

# pygame のセットアップ
pygame.init()
screen = pygame.display.set_mode(app.screen_size)
clock = pygame.time.Clock()  # アプリケーションの時間進行を監視するオブジェクトを作成

# ゲーム内で動くオブジェクトを用意
camera = camera.Camera(pygame.Vector2(0, 0), app.screen_size)
player = player.Player(pygame.Vector2(app.screen_size / 2), camera.scroll_velocity, app.screen_size)
enemies = []
for _ in range(10):
    enemies.append(enemy.Enemy())

game_objects = [camera, player]
game_objects.extend(enemies)

colliders = [player.collider]
for enemy in enemies:
    colliders.append(enemy.collider)

collision_manager = collision_manager.CollisionManager()
collision_manager.setup(colliders)

# 前フレームから何ミリ秒経過したか
dt = 0

running = True
while running:
    # event のポーリング
    for event in pygame.event.get():
        # pygame.QUIT: X を押してウィンドウを閉じられた
        if event.type == pygame.QUIT:
            running = False

    # 前のフレームの描画を塗りつぶして消す
    screen.fill(app.bg_fill_color)

    for go in game_objects:
        go.update(dt)

    collision_manager.collision_check()

    camera_pos = camera.position

    for go in game_objects:
        go.draw(screen, camera_pos)

    # スコアを表示する
    font = pygame.font.Font(None, 30)
    text = font.render(f'Score: {dt}', True, (255, 255, 255))
    screen.blit(text, pygame.Vector2(0, 0))

    # 描画内容を画面に反映する
    pygame.display.flip()

    # このメソッドを毎フレーム呼び出す. 引数を指定するとフレームレートの上限を設定できる.
    # 戻り値: 前回の呼び出しから何秒が経過したか
    dt = clock.tick(app.frame_rate) / 1000

pygame.quit()
