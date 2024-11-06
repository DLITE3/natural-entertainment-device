import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pytest
import os
import sys
from unittest.mock import MagicMock
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from  src.Wrapper.APIWrapper.spotify_web_api_handler import * #テストするファイルを参照
import requests

#インスタンスを作成
handler = SpotifyWebAPIHandler()
client_id = handler.get_client_id()
client_secret = handler.get_client_secret()
client_uri = handler.get_redirect_uri()


def test_play_track_mock_200(mocker):
    """
    play_trackメソッドがステータスコード200を返すことを確認するテスト
    """
    # モック用のトラックID
    track_id = "sample_track_id"
    # Spotify API呼び出しをモック
    mocker.patch.object(handler.sp, "start_playback", return_value=None)
    # 実際の再生を防ぎ、関数が問題なく実行されることを確認
    response = handler.play_track(track_id)
    assert response == 200  # ここはエラーハンドリングを追加する場合の例です

