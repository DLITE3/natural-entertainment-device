import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pytest
import os
import sys
from unittest.mock import patch,MagicMock
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from  src.Wrapper.APIWrapper.spotify_web_api_handler import * #テストするファイルを参照


@pytest.fixture
def spotify_handler():
    return SpotifyWebAPIHandler()

@patch("src.Wrapper.APIWrapper.spotify_web_api_handler.SpotifyWebAPIHandler.get_available_device_id")  # メソッドをモック
@patch("src.Wrapper.APIWrapper.spotify_web_api_handler.Spotify")  # Spotifyのインスタンスをモック
def test_get_available_device_id(mock_spotify, mock_get_device_id, spotify_handler):
    # モックデバイス情報を設定
    mock_device_response = {
        'devices': [
            {'id': 'device1', 'name': 'Device 1', 'type': 'phone'},
            {'id': 'device2', 'name': 'Device 2', 'type': 'laptop'}
        ]
    }

    # Spotifyインスタンスのdevicesメソッドをモック
    mock_spotify.return_value.devices.return_value = mock_device_response

    # ユーザー入力をモック
    with patch("builtins.input", return_value="1"):  # ユーザーが "1" を選択したと仮定
        device_id = spotify_handler.get_available_device_id()
    
    # get_available_device_idが期待通りに動作するかを確認
    assert device_id == 'device1'  # "1"が選ばれたのでdevice1が返るはず

@patch("src.Wrapper.APIWrapper.spotify_web_api_handler.SpotifyWebAPIHandler.get_available_device_id")  # メソッドをモック
@patch("src.Wrapper.APIWrapper.spotify_web_api_handler.Spotify")  # Spotifyのインスタンスをモック
def test_no_devices(mock_spotify, mock_get_device_id, spotify_handler):
    # デバイスがない場合のモック
    mock_device_response = {'devices': []}
    
    # Spotifyインスタンスのdevicesメソッドをモック
    mock_spotify.return_value.devices.return_value = mock_device_response
    
    # デバイスがない場合にget_available_device_idがどう動作するかテスト
    with patch("builtins.input", return_value="1"):
        device_id = spotify_handler.get_available_device_id()
    
    # デバイスがない場合はNoneを返すべき
    assert device_id is None
