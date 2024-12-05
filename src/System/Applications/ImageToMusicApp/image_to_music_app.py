from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from System.Applications.app import App
from System.Applications.ImageToMusicApp.picture_function import PictureFunction
from System.Applications.ImageToMusicApp.play_songs_function import PlaySongsFunction
from Wrapper import *


class ImageToMusicApp(App):
    def __init__(self):
        super().__init__()
        self.picture_func = PictureFunction()
        self.play_song_func = PlaySongsFunction()
        self.pins = [17, 22, 23, 27]
        self.buttons = ButtonWrapper(self.pins)
        self.buttons_data = None
        self.display = DisplayWrapper()
        
    
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
                image = self.picture_func.get_picture()
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
        self.camera.stop()
        self.display.stop()
        self.play_song_func.stop()
        
