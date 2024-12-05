from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.Wrapper.APIWrapper.image_to_song_api_wrapper import ImageToSongAPIWrapper

import cv2
import asyncio

async def main():
    image_to_song_api_wrapper: ImageToSongAPIWrapper = ImageToSongAPIWrapper()
    image = await asyncio.to_thread(cv2.imread, "OperationCheck/images/image.jpg")
    cv2.imshow("image", image)
    print(image_to_song_api_wrapper.image_to_song(image)["song_list"])

if __name__ == "__main__":
    asyncio.run(main())
