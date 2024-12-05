from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from System.Applications.app import App
from System.Applications.AudioToImageApp.audio_to_text import *
from System.Applications.AudioToImageApp.text_to_image import *
from Wrapper import *

import cv2
import time

class AudioToImageApp(App):
    def __init__(self):
        super().__init__()
        self.audio_to_text = AudioToText()
        self.text_to_image = TextToImage()
        self.mic = MicrophoneWrapper("USB PnP Sound Device: Audio (hw:3,0)")
        self.pins = [17, 22, 23, 27]
        self.buttons = ButtonWrapper(self.pins)
        self.buttons_data = None
        self.display = DisplayWrapper()

    def run(self) -> None:
        if not self.display.is_connected():
            return
        try:
            # 画面表示

            try:
                # ボタンの読み込み
                self.buttons_data = self.buttons.read_multiple_buttons()
                # print(self.buttons_data)
            except Exception as e:
                print(e)
            # 録音ボタンが押されたら
            if self.buttons_data[27] == 0:
                time.sleep(0.5)
                # 環境音を収音
                if self.mic.search_microphone():
                    self.mic.recording(duration=5)
                    time.sleep(0.3)
                # 環境音を言語化
                open_ai_query = self.audio_to_text.analyze_features("recording_filtered.wav")
                stable_diffusion_query = self.audio_to_text.audio_analyzing_data_to_text(open_ai_query)
                print(stable_diffusion_query)
                # 画像を生成
                self.text_to_image.generate_image(stable_diffusion_query)
                time.sleep(0.3)
                image = cv2.imread("output_image.jpeg")
                # 画像を90度右回転
                image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
                self.display.show_image(image)
            time.sleep(0.1)

        except Exception as e:
            print(e)
            self.stop()

    def is_finish(self) -> bool:
        return self.buttons_data[17] == 0

    def stop(self):
        self.display.stop()
        self.mic.stop()