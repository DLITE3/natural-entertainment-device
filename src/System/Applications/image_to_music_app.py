from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from System.Applications.app import App
from Wrapper import *
import cv2
import numpy as np
import time

class ImageToMusicApp(App):
    def __init__(self):
        super().__init__()
        self.spotify_web_api = SpotifyWebAPIWrapper()
        self.device_id = None
        self.camera = CameraWrapper()
        self.camera.start()
        self.display = DisplayWrapper()
        self.pins = [17, 22, 23, 27]
        self.buttons = ButtonWrapper(self.pins)
        self.buttons_data = None
        self.image_to_song_api = ImageToSongAPIWrapper()
    
    def run(self) -> None:
        if self.display.is_connected():
            try:
                image_data = self.camera.capture_image()
                image_array = np.frombuffer(image_data, np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                self.display.show_image(image)
                self.buttons_data = self.buttons.read_multiple_buttons()
                # print(self.buttons_data)
                if self.buttons_data[27] == 0:
                    print("take picture")
                    self.camera.take_picture()
                    time.sleep(1)
                    image = cv2.imread("image.jpg")
                    time.sleep(0.5)
                    songs = self.image_to_song_api.image_to_song(image)
                    song_id = None
                    for song in songs["song_list"]:
                        print(song)
                        song_id = self.spotify_web_api.search_track(song)
                        time.sleep(0.5)
                        if song_id != None:
                            print("song: " + song)
                            break
                    if song_id != None:
                        try:
                            devices = self.spotify_web_api.get_devices()
                            smart_phone_device_id = self.spotify_web_api.search_device("Smartphone", devices)
                            self.device_id = smart_phone_device_id
                            print("Smartphone id: " + smart_phone_device_id)
                            if smart_phone_device_id:
                                self.spotify_web_api.play_on_device(song_id, smart_phone_device_id)
                        except Exception as e:
                            print(e)
                            self.spotify_web_api.stop_playback(smart_phone_device_id)

            except Exception as e:
                self.stop()

    def is_finish(self) -> bool:
        return self.buttons_data[17] == 0

    def stop(self):
        self.camera.stop()
        self.display.stop()
        self.buttons.stop()
        self.spotify_web_api.stop_playback(self.device_id)
