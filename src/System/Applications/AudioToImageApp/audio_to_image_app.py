from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from System.Applications.app import App
from System.Applications.AudioToImageApp.audio_to_text import *
from System.Applications.AudioToImageApp.text_to_image import *
from Wrapper import *

class AudioToImageApp(App):
    def __init__(self):
        super().__init__()
        self.audio_to_text = AudioToText()
        self.text_to_image = TextToImage()
        self.mic = MicrophoneWrapper()
        self.pins = [17, 22, 23, 27]
        self.buttons = ButtonWrapper(self.pins)
        self.buttons_data = None

    def run(self) -> None:
        if not self.display.is_connected():
            return
        try:
            # カメラの実行
            self.picture_func.run_camera_func()

            # ボタンの読み込み
            self.buttons_data = self.buttons.read_multiple_buttons()
            # print(self.buttons_data)

            # 撮影ボタンが押されたら
            if self.buttons_data[27] == 0:
                # 画像を取得
                image = self.picture_func.get_picuture()
                # 画像から曲を検索
                song_id = self.play_song_func.select_song(image)
                # 曲を再生
                self.play_song_func.play_song(song_id, "Smartphone")
        except Exception as e:
            print(e)
            self.stop()

    def is_finish(self) -> bool:
        return self.buttons_data[17] == 0

    def stop(self):
        self.display.stop()
        self.buttons.stop()