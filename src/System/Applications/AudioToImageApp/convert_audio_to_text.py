import librosa
import numpy as np
import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from src.Wrapper.APIWrapper.openai_api_handler import OpenAIAPIHandler
import json


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

        self.api_handler = OpenAIAPIHandler()

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
            "スペクトログラムの最大値": np.max(self.spectrogram),
            "スペクトログラムの最小値": np.min(self.spectrogram),
            "エンベロープの平均強度": np.mean(self.envelope),
            "エンベロープの最大強度": np.max(self.envelope),
            "ゼロ交差率の平均": np.mean(self.zero_crossings),
            "ゼロ交差率の最大": np.max(self.zero_crossings),
            "スペクトル重心の平均": np.mean(self.spectral_centroid),
            "スペクトル重心の最大": np.max(self.spectral_centroid),
            "スペクトルフラットネスの平均": np.mean(self.spectral_flatness),
            "スペクトルフラットネスの最大": np.max(self.spectral_flatness),
            "エネルギーの平均": np.mean(self.energy),
            "エネルギーの最大": np.max(self.energy),
            "エネルギーの最小": np.min(self.energy),
        }

        return results

    def send_to_gpt(self, results):
        
       #特徴量を引数とし、GPTへリクエストを送る    
       response = self.api_handler.post_request(str(results) + "この音からどのような感情を受け取りますか？\
                                                テキストをそのままstable diffusionに入力したいので、特徴量の名称は言わず、英語で答えてください\
                                                「this sound」という言葉もいりません。\
                                                そして、感情を表す文のみをstable diffusionが入力しやすい形で答えてください。")
       return response.text
