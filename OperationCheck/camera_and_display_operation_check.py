from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.Wrapper.DeviceWrapper.camera_wrapper import CameraWrapper
from src.Wrapper.DeviceWrapper.display_wrapper import DisplayWrapper

import cv2
import numpy as np

def main():
    camera = CameraWrapper()
    camera.start()
    display: DisplayWrapper = DisplayWrapper()
    print(display.is_connected())

    if display.is_connected():
        # ループで画像を常時更新
        try:
            while True:
                # 画像を取得
                image_data = camera.capture_image()

                # OpenCVで表示するためにバイトデータをデコード
                image_array = np.frombuffer(image_data, np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

                display.show_image(image)
            
            camera.stop()
            display.stop()
                
        finally:
            # リソースを解放
            camera.stop()
            display.stop()

if __name__ == "__main__":
    main()

