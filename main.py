import pygame
import app_setting
from scene.scene_runner import SceneRunner
from scene.scene_type import SceneType

# pygame のセットアップ
pygame.init()
screen = pygame.display.set_mode(app_setting.screen_size)
clock = pygame.time.Clock()  # アプリケーションの時間進行を監視するオブジェクトを作成

scene_runner = SceneRunner()
scene_runner.request_change_scene(SceneType.Title)
scene_runner.start()

# 前フレームから何ミリ秒経過したか
dt = 0

while scene_runner.is_running:
    # event のポーリング
    for event in pygame.event.get():
        # X を押してウィンドウを閉じられた
        if event.type == pygame.QUIT:
            running = False

    # 前のフレームの描画を塗りつぶして消す
    screen.fill(app_setting.bg_fill_color)

    # ゲーム更新処理
    scene_runner.run(screen, dt)

    # 描画内容を画面に反映する
    pygame.display.flip()

    # このメソッドを毎フレーム呼び出す. 引数を指定するとフレームレートの上限を設定できる.
    # 戻り値: 前回の呼び出しから何秒が経過したか
    dt = clock.tick(app_setting.frame_rate) / 1000

pygame.quit()
