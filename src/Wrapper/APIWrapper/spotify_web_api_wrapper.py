import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

class SpotifyWebAPIWrapper:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
        self.scope = 'user-library-read user-modify-playback-state user-read-playback-state'
        # Spotify認証
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
                                                           client_secret=self.client_secret,
                                                           redirect_uri=self.redirect_uri,
                                                           scope=self.scope,
                                                           cache_path="/tmp/spotify_cache"))
         

    # 曲名でトラックIDを検索するメソッド
    def search_track(self, track_name):
        result = self.sp.search(q=track_name, type='track', limit=1)
        if result['tracks']['items']:
            track = result['tracks']['items'][0]
            track_id = track['id']
            track_name = track['name']
            # print(f"Found track: {track_name} (ID: {track_id})")
            return track_id
        else:
            # print(f"Track '{track_name}' not found.")
            return None

    # デバイス一覧を取得するメソッド
    def get_devices(self):
        devices = self.sp.devices()
        device_list = devices['devices']
        if not device_list:
            # print("No available devices found.")
            return None
        for device in device_list:
            print(f"Device: {device['name']} (ID: {device['id']})")
        return device_list
    
    def search_device(self, device_name, device_list):
        for device in device_list:
            if device['type'] == device_name:
                return device['id']
        return None

    # デバイスで曲を再生するメソッド
    def play_on_device(self, track_id, device_id):
        try:
            self.sp.start_playback(device_id=device_id, uris=[f"spotify:track:{track_id}"])
            # print(f"Playing track {track_id} on device {device_id}")
            return True
        except Exception as e:
            return (f"Error playing track: {e}")