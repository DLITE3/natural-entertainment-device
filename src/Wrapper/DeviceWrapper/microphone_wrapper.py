import pyaudio
import wave
import numpy as np
from scipy.signal import butter, lfilter

class MicrophoneWrapper:
    def __init__(self, micName: str):
        self.micName = micName
        self.audio = pyaudio.PyAudio()
        self.device_index = None
        self.sample_rate = 44100
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16
        self.output_file = "recording_filtered.wav"

    def search_microphone(self):
        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            if self.micName.lower() in device_info.get("name", "").lower():
                self.device_index = i
                print(f"Microphone '{self.micName}' found at index {i}.")
                return True
        print(f"Microphone '{self.micName}' not found.")
        return False

    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype="band")
        return b, a

    def apply_filter(self, data, lowcut, highcut):
        b, a = self.butter_bandpass(lowcut, highcut, self.sample_rate, order=6)
        return lfilter(b, a, data)

    def recording(self, duration: int = 5, lowcut: float = 100.0, highcut: float = 8000.0):
        if self.device_index is None:
            print("Microphone not set. Please run search_microphone() first.")
            return

        print(f"Recording for {duration} seconds...")
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            input_device_index=self.device_index,
            frames_per_buffer=self.chunk_size,
        )

        frames = []
        for _ in range(0, int(self.sample_rate / self.chunk_size * duration)):
            try:
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                frames.append(data)
            except OSError as e:
                print(f"Warning: {e}")
                frames.append(b'\x00' * self.chunk_size)

        print("Recording finished. Applying filter...")

        # Convert audio frames to NumPy array
        audio_data = np.frombuffer(b"".join(frames), dtype=np.int16)

        # Apply bandpass filter
        filtered_audio = self.apply_filter(audio_data, lowcut, highcut)

        print("Filter applied. Saving the file...")

        # Save filtered audio
        with wave.open(self.output_file, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(filtered_audio.astype(np.int16).tobytes())

        print(f"Filtered file saved as {self.output_file}.")
        self.stop()

    def stop(self):
        self.audio.terminate()
