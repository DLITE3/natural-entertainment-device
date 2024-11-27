import requests
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import os
load_dotenv()

class StableDiffusionWrapper:
    def __init__(self ):
        self.api_url = os.getenv("STABLE_DIFFUSION_API_URL")
        if not self.api_url:
            raise ValueError("STABLE_DIFFUSION_API_URL が設定されていません。")

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

    def post_data(self, prompt: str) -> Image.Image:
        """
        Stable Diffusion APIにプロンプトを送信して画像を生成する
        """
        data = {"query": prompt}
        response = requests.post(self.api_url, json=data)
        return response.json()

