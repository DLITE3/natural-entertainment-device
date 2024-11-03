from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# 環境変数をロード
load_dotenv()

class SpotifyWebAPIHandler:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        # クライアント認証をセットアップ
        self.client_credentials_manager = SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
    
    def search_and_get_play_url(self, query, search_type="track"):
        """
        Spotifyで指定したクエリを検索し、再生リンクを取得
        
        Args:
        - query (str): 検索したいクエリ（アーティスト名や曲名など）
        - search_type (str): 検索タイプ。通常は"track"（曲検索）
        
        Returns:
        - str: Spotify Webプレイヤーでの再生リンク
        """
        try:
            results = self.sp.search(q=query, type=search_type)
            if search_type == "track" and results['tracks']['items']:
                # 最初のトラックのIDを取得
                track_id = results['tracks']['items'][0]['id']
                track_name = results['tracks']['items'][0]['name']
                play_url = f"https://open.spotify.com/track/{track_id}"
                return f"{track_name} の再生リンク: {play_url}"
            else:
                return "指定したクエリで曲が見つかりませんでした。"
        except Exception as e:
            return f"エラーが発生しました: {e}"


"""

# インスタンスを作成し、再生リンクを取得 してみる
spotify_handler = SpotifyWebAPIHandler()
query = "高嶺の花子さん"  # 検索したい曲名
play_url = spotify_handler.search_and_get_play_url(query)
print(play_url)

"""