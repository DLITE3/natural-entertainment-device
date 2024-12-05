from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.System.Applications import *
from src.Wrapper.DeviceWrapper.display_wrapper import DisplayWrapper
from src.Wrapper.DeviceWrapper.button_wrapper import ButtonWrapper

from adafruit_rgb_display.rgb import color565
import cv2
import time

class System:
    def __init__(self):
        self.apps: List[App] = [
            AudioToImageApp(),
            ImageToMusicApp(),
        ]
        self.app_index = 0

        self.display = DisplayWrapper()
        self.draw_start_screen()

        self.select_app_images: List[cv2.imread] = [
            cv2.imread("src/images/select_sound_to_visual_art_app.jpg"),
            cv2.imread("src/images/select_photo_to_music_app.jpg"),
        ]

        self.buttons = ButtonWrapper([17, 22, 23, 27])

    def draw_start_screen(self) -> None:
        print("Start!")
        self.display.fill(color565(0, 0, 0))
        image = cv2.imread("src/images/start_image.jpg")
        # 90度左回転
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.display.show_image(image)
        time.sleep(2)
        self.display.fill(color565(0, 0, 0))

    def run(self) -> None:
        try:
            while True:
                while True:
                    image = cv2.rotate(self.select_app_images[self.app_index], cv2.ROTATE_90_COUNTERCLOCKWISE)
                    self.display.show_image(image)
                    buttons_data = self.buttons.read_multiple_buttons()

                    if buttons_data[23] == 0:
                        self.app_index = 0
                    elif buttons_data[22] == 0:
                        self.app_index = 1
                    elif buttons_data[27] == 0:
                        self.display.fill(color565(0, 0, 0))
                        break
                    time.sleep(0.1)

                while True:
                    self.apps[self.app_index].run()
                    if self.apps[self.app_index].is_finish():
                        print("finish")
                        self.apps[self.app_index].stop()
                        break
        except Exception as e:
            print(e)
            self.apps[self.app_index].stop()
