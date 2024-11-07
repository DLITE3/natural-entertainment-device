from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.Wrapper.DeviceWrapper.camera_wrapper import CameraWrapper

import cv2
import numpy as np

# メイン処理
camera = CameraWrapper()
camera.start()

# ループで画像を常時更新
try:
    while True:
        # 画像を取得
        image_data = camera.capture_image()

        # OpenCVで表示するためにバイトデータをデコード
        image_array = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        # 画像を表示
        cv2.imshow("Captured Image", image)

        # キーが押されたら終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # リソースを解放
    camera.stop()
    cv2.destroyAllWindows()
