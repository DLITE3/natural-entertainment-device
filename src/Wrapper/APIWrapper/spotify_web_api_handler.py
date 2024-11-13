#NTT名古屋用にスマートフォンから曲が再生されるように設定

from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# 環境変数の読み込み
load_dotenv()

class SpotifyWebAPIHandler:
    def __init__(self):
        # Spotify APIクライアント情報を環境変数から取得
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

        # 認証に必要なスコープ
        self.scope = "user-read-playback-state user-modify-playback-state user-library-read app-remote-control"

        # Spotify API認証ハンドラーを初期化
        self.auth_manager = self.initialize_auth_manager()
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

    def initialize_auth_manager(self):
        """
        SpotifyOAuthオブジェクトを初期化し、キャッシュ済みトークンのチェックや取得を行います。
        """
        auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_path=".spotify_token_cache"  # 認証情報をキャッシュするファイル
        )

        # キャッシュにトークンがあるかを確認し、存在しない場合は新しい認証を実行
        token_info = auth_manager.get_cached_token()
        if not token_info:
            print("キャッシュされているトークンが見つかりません。認証を実行中...")
            token_info = auth_manager.get_access_token(as_dict=False)

        #print("トークンが正常に取得されました。")
        return auth_manager

    def get_client_id(self):
        """クライアントIDを取得"""
        return self.client_id

    def get_client_secret(self):
        """クライアントシークレットを取得"""
        return self.client_secret

    def get_redirect_uri(self):
        """リダイレクトURIを取得"""
        return self.redirect_uri

    def get_available_device_id(self):
        """
        利用可能なデバイスIDを取得。複数デバイスがある場合はスマートフォンを優先して選択。
        
        Returns:
            str: 利用可能なデバイスID
        """
        try:
            devices = self.sp.devices()
            if devices['devices']:
                for device in devices['devices']:
                    if device['type'] == 'Smartphone':
                        return device['id']
                print("スマートフォンデバイスが見つかりませんでした。")
            else:
                print("利用可能なデバイスが見つかりません。Spotifyアプリを起動してください。")
        except Exception as e:
            print(f"デバイス取得中にエラーが発生しました: {e}")
        return None

    def search_track(self, query):
        """
        Spotify上で曲を検索し、最初の検索結果を返す。
        
        Args:
            query (str): 曲名またはアーティスト名
        
        Returns:
            dict: トラック情報（IDと名前）
        """
        try:
            results = self.sp.search(q=query, type="track", limit=1)
            if results['tracks']['items']:
                first_track = results['tracks']['items'][0]
                return {'id': first_track['id'], 'name': first_track['name']}
            print("指定した曲が見つかりませんでした。")
        except Exception as e:
            print(f"曲検索中にエラーが発生しました: {e}")
        return None

    def play_track(self, track_id):
        """
        指定されたトラックIDを再生する。
        
        Args:
            track_id (str): 再生するトラックのID
        """
        device_id = self.get_available_device_id()
        if not device_id:
            print("再生できるデバイスがありません。")
            return

        try:
            self.sp.start_playback(device_id=device_id, uris=[f"spotify:track:{track_id}"])
            #print("トラックを再生しています。")
            return 200
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 401:
                print("認証エラー: トークンが無効または期限切れです。再認証が必要です。")
            elif e.http_status == 403:
                print("再生エラー: プレミアムアカウントが必要です。")
            else:
                print(f"Spotify APIエラーが発生しました: {e}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")



#インスタンスを作成し、曲を検索して再生してみる

spotify_handler = SpotifyWebAPIHandler()
query = "henceforthorange"  # 検索したい曲名
# 曲を検索し、結果があれば再生
track_info = spotify_handler.search_track(query)
if track_info:
    spotify_handler.play_track(track_info['id'])


