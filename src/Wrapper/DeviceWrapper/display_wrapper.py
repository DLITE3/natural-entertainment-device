from adafruit_rgb_display.rgb import color565
from adafruit_rgb_display.ili9341 import ILI9341
from busio import SPI
from digitalio import DigitalInOut
import board
from PIL import Image
import cv2

class DisplayWrapper:
    # コンストラクタ
    def __init__(self):
        # print("DisplayWrapper:__init__")
        try:
            # Pin Configuration
            cs_pin = DigitalInOut(board.D8)
            dc_pin = DigitalInOut(board.D25)
            rst_pin = DigitalInOut(board.D24)

            # Set up SPI bus
            spi = SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

            # Create the ILI9341 display:
            self.disp = ILI9341(
                spi,
                cs=cs_pin, dc=dc_pin, rst=rst_pin,
                width=240, height=320,
                rotation=90,
                baudrate=24000000
            )

            # Define image size (320x240, rotated)
            self.IMAGE_SIZE = (self.disp.height, self.disp.width)
            self.connected = True
        except Exception as e:
            print(f"Display connection failed: {e}")
            self.connected = False

    def is_connected(self) -> bool:
        return self.connected

    def show_image(self, image) -> None:
        if image is None or not self.connected:
            return

        # OpenCVで読み込んだ画像はBGR形式なので、RGBに変換
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # NumPy配列をPIL画像に変換
        pil_image = Image.fromarray(image_rgb)

        # 必要に応じて上下反転
        pil_image = pil_image.transpose(Image.FLIP_TOP_BOTTOM)
        
        # 90度左回転
        pil_image = pil_image.rotate(90, expand=True)

        # 左右反転
        pil_image = pil_image.transpose(Image.FLIP_LEFT_RIGHT)

        # 画面サイズにリサイズ
        pil_image = pil_image.resize(self.IMAGE_SIZE, resample=Image.LANCZOS)

        if self.connected:
            # 画像を表示
            self.disp.image(pil_image)

    def draw_rect(self, x: int, y: int, width: int, height: int, color) -> None:
        if self.connected:
            self.disp.fill_rectangle(x, y, width, height, color)

    def fill(self, color) -> None:
        if self.connected:
            self.disp.fill(color)

    def stop(self) -> None:
        if self.connected:
            self.disp.fill(0)