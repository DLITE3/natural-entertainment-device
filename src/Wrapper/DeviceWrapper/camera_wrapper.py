from picamera2 import Picamera2
from PIL import Image
from io import BytesIO
from time import sleep
import cv2
import numpy as np

class CameraWrapper:
    def __init__(self):
        self.camera = Picamera2()

    def start(self) -> None:
        config = self.camera.create_still_configuration(main={"size": (640, 480)})
        self.camera.configure(config)
        self.camera.start()
        sleep(2)

    def capture_image(self) -> bytes:
        # 画像をキャプチャしてバイトデータに変換
        image_array = self.camera.capture_array()
        image = Image.fromarray(image_array)
        
        byte_io = BytesIO()
        image.save(byte_io, 'JPEG')
        byte_io.seek(0)

        return byte_io.getvalue()
    
    def take_picture(self) -> None:
        image_data = self.capture_image()
        image_array = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        # 右回転90度で保存
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite("image.jpg", image)
    
    def stop(self) -> None:
        self.camera.stop()

