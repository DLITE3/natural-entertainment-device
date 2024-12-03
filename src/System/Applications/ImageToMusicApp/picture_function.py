from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from Wrapper import *
import cv2
import time

class PictureFunction:
    def __init__(self) -> None:
        self.spotify_web_api = SpotifyWebAPIWrapper()
        self.device_id = None
        self.camera = CameraWrapper()
        self.camera.start()
        self.display = DisplayWrapper()
        pass

    def run_camera_func(self) -> None:
        image_data = self.camera.capture_image()
        image_array = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        self.display.show_image(image)

    def get_picture(self) -> np.ndarray:
        print("take picture")
        self.camera.take_picture()
        time.sleep(1)
        image = cv2.imread("image.jpg")
        time.sleep(0.5)
        return image