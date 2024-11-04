from dotenv import load_dotenv
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# 環境変数をロード
load_dotenv()

class SpotifyWebAPIHandler:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

        # スコープに再生コントロールとライブラリアクセスを追加
        scope = "user-read-playback-state user-modify-playback-state user-library-read app-remote-control"

        # OAuth認証をセットアップ（キャッシュ機能付き）
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=scope,
            cache_path=".spotify_token_cache"  # トークンキャッシュファイル
        ))

    def get_available_device_id(self):
        """
        利用可能なデバイスIDを取得。複数デバイスがある場合は手動選択。
        
        Returns:
        - str: 選択されたデバイスのID
        """
        try:
            devices = self.sp.devices()
            if devices['devices']:
                print("利用可能なデバイス:")
                for idx, device in enumerate(devices['devices']):
                    print(f"{idx + 1}: {device['name']} - {device['type']}")

                choice = int(input("再生するデバイス番号を選んでください: ")) - 1
                return devices['devices'][choice]['id']
            else:
                print("再生可能なデバイスが見つかりません。Spotifyアプリを起動してください。")
                return None
        except Exception as e:
            print(f"エラーが発生しました（デバイス取得中）: {e}")
            return None

    def search_track(self, query):
        """
        指定したクエリのトラックを検索し、最初の結果を返す。
        
        Args:
        - query (str): 検索したい曲のクエリ
        
        Returns:
        - dict: トラック情報（IDと名前）
        """
        try:
            # トラックを検索
            results = self.sp.search(q=query, type="track", limit=1)
            if results['tracks']['items']:
                # 最初のトラックを取得
                first_track = results['tracks']['items'][0]
                track_info = {
                    'id': first_track['id'],
                    'name': first_track['name']
                }
                print(f"検索結果: {track_info['name']}")
                return track_info
            else:
                print("指定した曲が見つかりませんでした。")
                return None
        except Exception as e:
            print(f"エラーが発生しました（検索中）: {e}")
            return None

    def play_track(self, track_id):
        """
        指定したトラックIDを再生する。
        
        Args:
        - track_id (str): 再生したいトラックのID
        """
        try:
            # 利用可能なデバイスIDを取得
            device_id = self.get_available_device_id()
            if device_id:
                # 再生を開始
                self.sp.start_playback(device_id=device_id, uris=[f"spotify:track:{track_id}"])
                print("トラックを再生しています。")
                
                # 再生状態を確認し、曲が終わったら停止
                while True:
                    playback_info = self.sp.current_playback()
                    if playback_info is None or playback_info['is_playing'] is False:
                        print("曲が終了しました。")
                        break
                    time.sleep(1)  # 1秒ごとに状態をチェック
            else:
                print("再生できるデバイスがありません。")
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 401:
                print("認証エラー: トークンが無効または期限切れです。再認証が必要です。")
            elif e.http_status == 403:
                print("再生エラー: プレミアムアカウントが必要です。")
            else:
                print(f"Spotify APIでエラーが発生しました: {e}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")



"""　インスタンスを作成し、曲を検索して再生してみる

spotify_handler = SpotifyWebAPIHandler()
query = "henceforthorange"  # 検索したい曲名
# 曲を検索し、結果があれば再生
track_info = spotify_handler.search_track(query)
if track_info:
    spotify_handler.play_track(track_info['id'])

"""