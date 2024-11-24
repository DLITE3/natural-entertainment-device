import requests
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import os
load_dotenv()

class StableDiffusionWrapper:
    def __init__(self, ):
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

    def generate_image(self, prompt: str) -> Image.Image:
        """
        Stable Diffusion APIにプロンプトを送信して画像を生成する
        """
        data = {"query": prompt}
        try:
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()
            response_data = response.json()
        except requests.RequestException as e:
            print(f"Error sending request to API: {e}")
            raise

        base64_image = response_data.get("image")
        if base64_image:
            return self.base64_to_image(base64_image)
        else:
            raise ValueError("レスポンスに画像データが含まれていません。")

