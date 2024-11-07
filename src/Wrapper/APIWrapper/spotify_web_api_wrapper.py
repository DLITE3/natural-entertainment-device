import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import time

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
                                                           scope=self.scope))

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
        # for device in device_list:
        #     print(f"Device: {device['name']} (ID: {device['id']})")
        return device_list
    
    # デバイス名でIDを検索するメソッド
    def search_device(self, device_name: str, device_list):
        for device in device_list:
            if device['type'] == device_name:
                return device['id']
        return None

    # デバイスで曲を再生するメソッド
    def play_on_device(self, track_id, device_id):
        try:
            self.sp.start_playback(device_id=device_id, uris=[f"spotify:track:{track_id}"])
            # リピートしない
            self.sp.repeat('off')
            self.sp.volume(100, device_id=device_id)
            # print(f"Playing track {track_id} on device {device_id}")
            return {"status_code": 200, "message": f"Playing track {track_id} on device {device_id}"}
        except Exception as e:
            # print(f"Error playing track: {e}")
            return {"status_code": 500, "message": f"Error playing track: {e}"}

    # 再生を停止するメソッド
    def stop_playback(self, device_id):
        try:
            self.sp.pause_playback(device_id=device_id)
            # print(f"Playback stopped on device {device_id}")
            return {"status_code": 200, "message": f"Playback stopped on device {device_id}"}
        except Exception as e:
            # print(f"Error stopping playback: {e}")
            return {"status_code": 500, "message": f"Error stopping playback: {e}"}