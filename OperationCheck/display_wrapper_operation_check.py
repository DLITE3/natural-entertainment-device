from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.Wrapper.DeviceWrapper.display_wrapper import DisplayWrapper

import cv2
import time

def main():
    display: DisplayWrapper = DisplayWrapper()
    print(display.is_connected())

    if display.is_connected():
        image_path = str(Path(__file__).resolve().parent / "images" / "image.jpg")
        image = cv2.imread(image_path)

        display.show_image(image)
        time.sleep(5)

    display.stop()

if __name__ == "__main__":
    main()