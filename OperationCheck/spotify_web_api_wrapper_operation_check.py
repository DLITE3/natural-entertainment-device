from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.Wrapper.APIWrapper.spotify_web_api_wrapper import SpotifyWebAPIWrapper

def main():
    spotify_handler = SpotifyWebAPIWrapper()
    query = "ルマ"  # 検索したい曲名
    # 曲を検索し、結果があれば再生
    track_info = spotify_handler.search_track(query)
    print(track_info)
    devices = spotify_handler.get_devices()
    smart_phone_device = spotify_handler.serch_devie("Smartphone", devices)
    print(smart_phone_device)
    if smart_phone_device and track_info:
        spotify_handler.play_on_device(track_info, smart_phone_device)

if __name__ == "__main__":
    main()