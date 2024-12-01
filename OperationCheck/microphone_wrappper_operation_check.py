from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.Wrapper.DeviceWrapper.microphone_wrapper import MicrophoneWrapper

def main() -> None:
    mic = MicrophoneWrapper("USB PnP Sound Device: Audio (hw:3,0)")
    if mic.search_microphone():
        mic.recording(duration=10)
    mic.close()

if __name__ == "__main__":
    main()