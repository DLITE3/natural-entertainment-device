import requests
from dotenv import load_dotenv
import os

load_dotenv()

class OpenAIAPIWrapper:
    def __init__(self) -> None:
        self.api_url = os.getenv("OPENAI_API_URL")

    def post_request(self, query: str) -> requests.Response:
        # POSTリクエストを送信
        response = requests.post(
            self.api_url,
            json={
                "query": query,
            }
        )

        # レスポンスの内容を表示
        return response
