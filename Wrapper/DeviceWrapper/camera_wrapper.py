from picamera2 import Picamera2
from PIL import Image
from io import BytesIO
from time import sleep

class CameraWrapper:
    def __init__(self):
        self.camera = Picamera2()

    def start(self) -> None:
        self.camera.configure(self.camera.create_still_configuration())
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
    
    def stop(self) -> None:
        self.camera.stop()
