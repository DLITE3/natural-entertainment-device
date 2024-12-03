from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.System.Applications import *

class System:
    def __init__(self):
        self.apps: List[App] = [
            ImageToMusicApp(),
            AudioToImageApp(),
        ]
        self.app_index = 1

    def run(self) -> None:
        try:
            while True:
                self.apps[self.app_index].run()
                if self.apps[self.app_index].is_finish():
                    print("finish")
                    self.apps[self.app_index].stop()
                    break
        except Exception as e:
            print(e)
            self.apps[self.app_index].stop()
