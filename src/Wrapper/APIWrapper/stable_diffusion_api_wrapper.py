from dotenv import load_dotenv
import os

load_dotenv()

import requests
import base64
from io import BytesIO
from PIL import Image

class StableDiffusionWrapper:
    def __init__(self):
        self.stable_diffusion_api_url = os.getenv("STABLE_DIFFUSION_API_URL")
        if self.stable_diffusion_api_url == None:
            raise ValueError("STABLE_DIFFUSION_API_URL is None.")

    def base64_to_image(self, base64_string: str) -> Image.Image:
        """
        Base64文字列をPillowのImageオブジェクトに変換する
        """
        try:
            image_data = base64.b64decode(base64_string)
            image_buffer = BytesIO(image_data)
            image = Image.open(image_buffer)
            return image
        except Exception as e:
            print(f"Error decoding Base64 string: {e}")
            raise

    def text_to_image(self, prompt: str) -> Image.Image:
        data = {
            "query": prompt
        }
        response = requests.post(self.stable_diffusion_api_url, json=data)
        return response.json()

    def save_generate_image(self, base64_image: str) -> None:
        if base64_image:
            # Base64文字列をバイナリデータに変換
            image_data = base64.b64decode(base64_image)

            # 画像ファイルとして保存
            with open("output_image.jpeg", "wb") as f:
                f.write(image_data)
            print("画像が保存されました: output_image.jpeg")
        else:
            print("画像データがレスポンスに含まれていません。")
