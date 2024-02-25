import pygame
import app_setting
from game_objects import camera, player
from main_game import MainGame

# pygame のセットアップ
pygame.init()
screen = pygame.display.set_mode(app_setting.screen_size)
clock = pygame.time.Clock()  # アプリケーションの時間進行を監視するオブジェクトを作成

# ゲーム内で動くオブジェクトを用意
camera = camera.Camera(pygame.Vector2(0, 0), app_setting.screen_size)
player = player.Player(pygame.Vector2(app_setting.screen_size / 2), camera.scroll_velocity, app_setting.screen_size)

# 前フレームから何ミリ秒経過したか
dt = 0

main_game = MainGame(player, camera)

running = True
while running:
    # event のポーリング
    for event in pygame.event.get():
        # X を押してウィンドウを閉じられた
        if event.type == pygame.QUIT:
            running = False

    # 前のフレームの描画を塗りつぶして消す
    screen.fill(app_setting.bg_fill_color)

    # ゲーム更新処理
    main_game.update(screen, dt)

    # 描画内容を画面に反映する
    pygame.display.flip()

    # このメソッドを毎フレーム呼び出す. 引数を指定するとフレームレートの上限を設定できる.
    # 戻り値: 前回の呼び出しから何秒が経過したか
    dt = clock.tick(app_setting.frame_rate) / 1000

pygame.quit()
