from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.Wrapper.APIWrapper.spotify_web_api_handler import SpotifyWebAPIHandler
import time

def main():
    spotify_handler = SpotifyWebAPIHandler()
    query = "45秒"  # 検索したい曲名
    # 曲を検索し、結果があれば再生
    track_info = spotify_handler.search_track(query)
    print("song id: " + track_info)
    # devices = spotify_handler.get_devices()
    # smart_phone_device_id = spotify_handler.get_available_device_id(devices)
    # print("Smartphone id: " + smart_phone_device_id)
    if track_info:
        try:
            spotify_handler.play_track(track_info['id'])
        except Exception as e:
            print(e)
            # spotify_handler.stop_playback(smart_phone_device_id)

if __name__ == "__main__":
    main()