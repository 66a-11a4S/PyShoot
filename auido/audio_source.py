# pygame.mixer.Sound をそのまま使うとファイルが読み込めないときの例外処理が必要なのでラップする
import pygame


class AudioSource:
    def __init__(self, resource_path, is_music=False):
        self._is_music = is_music
        try:
            if is_music:
                pygame.mixer_music.load(resource_path)
            else:
                self._sound_instance = pygame.mixer.Sound(resource_path)
            self._load_succeeded = True
        except FileNotFoundError:
            self._sound_instance = None
            self._load_succeeded = False

    def play(self, channel=None):
        if not self._load_succeeded:
            return

        if self._is_music:
            pygame.mixer_music.play()
        else:
            if channel is None:
                self._sound_instance.play()
            else:
                channel.play(self._sound_instance)

    def stop(self):
        if not self._load_succeeded:
            return

        if self._is_music:
            pygame.mixer_music.stop()
        else:
            self._sound_instance.stop()
