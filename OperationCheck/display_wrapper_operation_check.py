from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.Wrapper.DeviceWrapper import *

def main():
    display: DisplayWrapper = DisplayWrapper()

if __name__ == "__main__":
    main()