from dotenv import load_dotenv
import os

load_dotenv()

import requests
import re
import json

class ImageToSongAPIWrapper:
    # コンストラクタ
    def __init__(self):
        self.image_to_song_api_url = os.getenv("IMAGE_TO_SONG_API_URL")

    def image_to_song(self, image) -> object:
        response = requests.post(
            self.image_to_song_api_url,
            files={"file": image}
        )
        print("status_code: " + str(response.status_code))
        print(response.text)

        json_string_match = re.findall(r'\[.*?\]', response.text, re.DOTALL)

        if json_string_match:
            # 抽出された文字列の整形
            json_string = json_string_match[0].replace('\\"', '"').replace('\\n', '')

            # JSONをデコードして配列に変換
            song_list = json.loads(json_string)
            return {"song_list": song_list, "status_code": response.status_code}
        else:
            # print("JSON配列部分が見つかりませんでした。")
            return {"song_list": None, "status_code": response.status_code}
