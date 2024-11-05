from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.Wrapper.DeviceWrapper.display_wrapper import DisplayWrapper

def main():
    display: DisplayWrapper = DisplayWrapper()
    print(display.is_active())
    display.stop()

if __name__ == "__main__":
    main()