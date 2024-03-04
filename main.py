import pygame
import app_setting
from auido.channel_id import ChannelType
from input.input_handler import InputHandler
from input.input_status import InputStatus
from scene.scene_runner import SceneRunner
from scene.scene_type import SceneType

# pygame のセットアップ
pygame.init()
screen = pygame.display.set_mode(app_setting.screen_size)
clock = pygame.time.Clock()  # アプリケーションの時間進行を監視するオブジェクトを作成

# 優先して鳴らしたい音のチャンネル数を事前に確保し、確実に優先音が鳴るようにしておく
pygame.mixer.set_reserved(ChannelType.ReservedChannels.value[0])

scene_runner = SceneRunner()
scene_runner.request_change_scene(SceneType.Title)
scene_runner.start()

# 前フレームから何ミリ秒経過したか
dt = 0
is_running = True

while is_running:

    # 入力イベントの更新
    InputHandler().update()
    is_running = not InputStatus().selected_close
    if not is_running:
        break

    # 前のフレームの描画を塗りつぶして消す
    screen.fill(app_setting.bg_fill_color)

    # ゲーム更新処理
    scene_runner.run(screen, dt)

    # 描画内容を画面に反映する
    pygame.display.flip()

    # このメソッドを毎フレーム呼び出す. 引数を指定するとフレームレートの上限を設定できる.
    # 戻り値: 前回の呼び出しから何秒が経過したか
    dt = clock.tick(app_setting.frame_rate) / 1000

    is_running = scene_runner.is_running

pygame.quit()
