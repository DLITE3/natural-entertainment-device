from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from Wrapper import *
import cv2
import asyncio
import time

class PlaySongsFunction:
    def __init__(self) -> None:
        self.image_to_song_api = ImageToSongAPIWrapper()

    async def select_song(self, image) -> str:
        songs = self.image_to_song_api.image_to_song(image)
        song_id = None
        for song in songs["song_list"]:
            print(song)
            song_id = self.spotify_web_api.search_track(song)
            time.sleep(0.5)
            if song_id != None:
                print("song: " + song)
                break
        return song_id
    
    def play_song(self, song_id, serch_device_name: str) -> None:
        if song_id != None:
            try:
                devices = self.spotify_web_api.get_devices()
                smart_phone_device_id = self.spotify_web_api.search_device(serch_device_name, devices)
                self.device_id = smart_phone_device_id
                print(serch_device_name + " id: " + smart_phone_device_id)
                if smart_phone_device_id:
                    self.spotify_web_api.play_on_device(song_id, smart_phone_device_id)
            except Exception as e:
                print(e)
                self.spotify_web_api.stop_playback(smart_phone_device_id)

    def stop(self):
        self.spotify_web_api.stop_playback(self.device_id)