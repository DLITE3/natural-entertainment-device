from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.Wrapper.DeviceWrapper.button_wrapper import ButtonWrapper

import time

def main():
    button_wrapper = ButtonWrapper([17, 22, 23, 27])
    try:
        while True:
            print(button_wrapper.read_multiple_buttons())
            time.sleep(0.1)
    except KeyboardInterrupt:
        button_wrapper.stop()

if __name__ == "__main__":
   main()