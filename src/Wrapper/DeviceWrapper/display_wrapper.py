from adafruit_rgb_display.rgb import color565
from adafruit_rgb_display.ili9341 import ILI9341

from busio import SPI
from digitalio import DigitalInOut
import board

from PIL import Image


class DisplayWrapper:
    # 成城接続時のSPIaddress
    CONNECT_OK: int = 548466237520

    # コンストラクタ
    def __init__(self):
        print("LcdWrapper:__init__")
        # Pin Configuration
        cs_pin = DigitalInOut(board.D8)
        dc_pin = DigitalInOut(board.D25)
        rst_pin = DigitalInOut(board.D24)

        # Set up SPI bus
        self.spi = SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

        # Create the ILI9341 display:
        self.disp = ILI9341(
            self.spi,
            cs=cs_pin, dc=dc_pin, rst=rst_pin,
            width=240, height=320,
            rotation=90,
            baudrate=24000000
        )

        # Define image size (320x240, rotated)
        self.IMAGE_SIZE = (self.disp.height, self.disp.width)

    def is_active(self) -> bool:
        print(id(self.disp))
        return id(self.spi) == self.CONNECT_OK

    def show_image(self, image):
        if image is None:
            return
        image = Image.fromarray(image)
        # Resize to screen size
        image = image.resize(self.IMAGE_SIZE, resample=Image.LANCZOS)

        # Display image
        self.disp.image(image)

    def stop(self):
        self.disp.fill(0)