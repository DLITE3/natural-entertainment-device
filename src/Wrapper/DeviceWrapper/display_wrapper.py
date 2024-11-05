from adafruit_rgb_display.ili9341 import ILI9341
from busio import SPI
from digitalio import DigitalInOut
import board
from PIL import Image

class DisplayWrapper:
    # コンストラクタ
    def __init__(self):
        print("DisplayWrapper:__init__")
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
        image = Image.fromarray(image)
        # Resize to screen size
        image = image.resize(self.IMAGE_SIZE, resample=Image.LANCZOS)

        # Display image
        self.disp.image(image)

    def stop(self) -> None:
        if self.connected:
            self.disp.fill(0)
            self.disp.show()
