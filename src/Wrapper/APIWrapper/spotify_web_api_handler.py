from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# 環境変数をロード
load_dotenv()

class SpotifyWebAPIHandler:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

        # スコープに再生コントロールを追加
        scope = "user-read-playback-state user-modify-playback-state"

        # OAuth認証をセットアップ
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=scope
        ))

    def get_available_device_id(self):
        """
        利用可能なデバイスIDを取得
        
        Returns:
        - str: 利用可能なデバイスのID
        """
        devices = self.sp.devices()
        if devices['devices']:
            # 最初の利用可能なデバイスIDを取得
            return devices['devices'][0]['id']
        else:
            print("再生可能なデバイスが見つかりません。Spotifyアプリを起動してください。")
            return None

    def search_and_play_track(self, query):
        """
        指定したクエリのトラックを検索し、最初の結果をプレイ
        
        Args:
        - query (str): 再生したい曲の検索クエリ
        """
        try:
            # トラックを検索
            results = self.sp.search(q=query, type="track", limit=1)
            if results['tracks']['items']:
                # 最初のトラックIDを取得
                track_id = results['tracks']['items'][0]['id']
                track_name = results['tracks']['items'][0]['name']

                # 利用可能なデバイスIDを取得
                device_id = self.get_available_device_id()
                if device_id:
                    # 再生を開始
                    self.sp.start_playback(device_id=device_id, uris=[f"spotify:track:{track_id}"])
                    print(f"{track_name} を再生しています。")
                else:
                    print("再生できるデバイスがありません。")
            else:
                print("指定した曲が見つかりませんでした。")
        except Exception as e:
            print(f"エラーが発生しました: {e}")

# インスタンスを作成し、曲を再生
spotify_handler = SpotifyWebAPIHandler()
query = "高嶺の花子さん"  # 検索したい曲名
spotify_handler.search_and_play_track(query)