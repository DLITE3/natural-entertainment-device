from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from src.Wrapper.APIWrapper.openai_api_wrapper import OpenAIAPIWrapper

import librosa
import numpy as np
import os
import json

class AudioToText:
    def __init__(self):
        """
        初期化メソッド
        :param audio_path: 解析対象の音声ファイルのパス
        """
        self.y = None  # 音声データ
        self.sr = None  # サンプリングレート
        self.spectrogram = None  # スペクトル分布（パワースペクトログラム）
        self.envelope = None  # エンベロープ
        self.zero_crossings = None  # ゼロ交差率
        self.spectral_centroid = None  # スペクトル重心
        self.spectral_flatness = None  # スペクトルフラットネス
        self.energy = None  # エネルギー

        self.open_ai_api_wrapper = OpenAIAPIWrapper()

    def load_audio(self, audio_path: str) -> None:
        """
        音声データを読み込む
        """
        y, sr = librosa.load(audio_path, sr=None)
        return y, sr

    def analyze_features(self, audio_path: str) -> object:
        """
        音響特徴量を計算する
        """

        # 音声データを読み込む
        _y, _sr = self.load_audio(audio_path)

        # スペクトル分布（パワースペクトログラム）
        S = np.abs(librosa.stft(_y))**2
        self.spectrogram = librosa.amplitude_to_db(S, ref=np.max)

        # エンベロープ（振幅包絡線）
        self.envelope = librosa.onset.onset_strength(y=_y, sr=_sr)

        # ゼロ交差率
        self.zero_crossings = librosa.feature.zero_crossing_rate(_y)[0]

        # スペクトル重心
        self.spectral_centroid = librosa.feature.spectral_centroid(y=_y, sr=_sr)[0]

        # スペクトルフラットネス
        self.spectral_flatness = librosa.feature.spectral_flatness(y=_y)[0]

        # エネルギー
        self.energy = np.sum(S, axis=0)

        # 特徴量のまとめ
        results = {
            "Spectrogram Max Value": np.max(self.spectrogram),
            "Spectrogram Min Value": np.min(self.spectrogram),
            "Envelope Mean Intensity": np.mean(self.envelope),
            "Envelope Max Intensity": np.max(self.envelope),
            "Zero Crossing Rate Mean": np.mean(self.zero_crossings),
            "Zero Crossing Rate Max": np.max(self.zero_crossings),
            "Spectral Centroid Mean": np.mean(self.spectral_centroid),
            "Spectral Centroid Max": np.max(self.spectral_centroid),
            "Spectral Flatness Mean": np.mean(self.spectral_flatness),
            "Spectral Flatness Max": np.max(self.spectral_flatness),
            "Energy Mean": np.mean(self.energy),
            "Energy Max": np.max(self.energy),
            "Energy Min": np.min(self.energy),
        }

        return results

    def audio_analyzing_data_to_text(self, audio_analyzing_data: str) -> str:   
        #特徴量を引数とし、GPTへリクエストを送る    
        response = self.open_ai_api_wrapper.post_request(
            str(audio_analyzing_data) + \
            "\
                This is the result of analyzing the spectrum and energy of recorded environmental sounds.\
                Describe this sound in 30 words or less in emotional terms.\
                Please take into account that this result will be entered into the “Stable diffusion api” prompt to generate an image.\
            "
        )
        return response.text
