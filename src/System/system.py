from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.System.Applications import *

class System:
    def __init__(self):
        self.image_to_music_app: App = ImageToMusicApp()
        pass

    def run(self) -> None:
        try:
            while True:
                self.image_to_music_app.run()
                if self.image_to_music_app.is_finish():
                    print("finish")
                    self.image_to_music_app.stop()
                    break
        except Exception as e:
            print(e)
            self.image_to_music_app.stop()
