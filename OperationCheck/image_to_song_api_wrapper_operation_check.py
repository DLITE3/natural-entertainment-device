from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.Wrapper.APIWrapper.image_to_song_api_wrapper import ImageToSongAPIWrapper

import cv2

def main():
    # API ラッパーの使用
    image_to_song_api_wrapper = ImageToSongAPIWrapper()
    with open("OperationCheck/images/image.jpg", "rb") as image:
        print(image_to_song_api_wrapper.image_to_song(image)["song_list"])

if __name__ == "__main__":
    main()
