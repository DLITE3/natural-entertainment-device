import librosa
import numpy as np
import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from src.Wrapper.APIWrapper.openai_api_handler import OpenAIAPIHandler


class ConvertSoundToLanguage:
    def __init__(self, audio_path):
        """
        初期化メソッド
        :param audio_path: 解析対象の音声ファイルのパス
        """
        self.audio_path = audio_path
        self.y = None  # 音声データ
        self.sr = None  # サンプリングレート
        self.spectrogram = None  # スペクトル分布（パワースペクトログラム）
        self.envelope = None  # エンベロープ
        self.zero_crossings = None  # ゼロ交差率
        self.spectral_centroid = None  # スペクトル重心
        self.spectral_flatness = None  # スペクトルフラットネス
        self.energy = None  # エネルギー

    def load_audio(self):
        """
        音声データを読み込む
        """
        self.y, self.sr = librosa.load(self.audio_path, sr=None)

    def analyze_features(self):
        """
        音響特徴量を計算する
        """
        # スペクトル分布（パワースペクトログラム）
        S = np.abs(librosa.stft(self.y))**2
        self.spectrogram = librosa.amplitude_to_db(S, ref=np.max)

        # エンベロープ（振幅包絡線）
        self.envelope = librosa.onset.onset_strength(y=self.y, sr=self.sr)

        # ゼロ交差率
        self.zero_crossings = librosa.feature.zero_crossing_rate(self.y)[0]

        # スペクトル重心
        self.spectral_centroid = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)[0]

        # スペクトルフラットネス
        self.spectral_flatness = librosa.feature.spectral_flatness(y=self.y)[0]

        # エネルギー
        self.energy = np.sum(S, axis=0)

        # 特徴量のまとめ
        results = {
            "Spectrogram Max (dB)": np.max(self.spectrogram),
            "Spectrogram Min (dB)": np.min(self.spectrogram),
            "Envelope Mean": np.mean(self.envelope),
            "Envelope Max": np.max(self.envelope),
            "Zero Crossing Rate Mean": np.mean(self.zero_crossings),
            "Zero Crossing Rate Max": np.max(self.zero_crossings),
            "Spectral Centroid Mean (Hz)": np.mean(self.spectral_centroid),
            "Spectral Centroid Max (Hz)": np.max(self.spectral_centroid),
            "Spectral Flatness Mean": np.mean(self.spectral_flatness),
            "Spectral Flatness Max": np.max(self.spectral_flatness),
            "Energy Mean": np.mean(self.energy),
            "Energy Max": np.max(self.energy),
            "Energy Min": np.min(self.energy),
        }

        return results

    def send_to_gpt(self, results):
        
        #特徴量を引数とし、GPTへリクエストを送る    
        
        response = OpenAIAPIHandler.post_request(self, str(results))
        return response



