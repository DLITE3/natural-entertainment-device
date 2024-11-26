import requests
from dotenv import load_dotenv
import os

load_dotenv()

class OpenAIAPIHandler:
    def __init__(self):
        self.api_url = os.getenv("OPENAI_API_URL")

    def post_request(self, query: str):
        # POSTリクエストを送信
        response = requests.post(
            self.api_url,
            json={
                "query": query,
                "additional_text": "この音を聞くと、どのような感情を受け取りますか？\
                    stable diffusionにテキストをそのまま使うので、stable diffusionが入力しやすい形だけで答えてください。"
            }
        )

        # レスポンスの内容を表示
        return response
