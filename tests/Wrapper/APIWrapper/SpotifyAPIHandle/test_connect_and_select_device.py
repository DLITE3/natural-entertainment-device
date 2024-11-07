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
    """SpotifyWebAPIHandlerのインスタンスを返すfixture"""
    return SpotifyWebAPIHandler()

def test_get_available_device_id_with_smartphone(spotify_handler):
    """スマートフォンデバイスが見つかる場合のテスト"""
    # モックデータ
    mock_devices = {
        'devices': [
            {'name': 'PC', 'type': 'Computer', 'id': 'pc123'},
            {'name': 'Smartphone', 'type': 'Smartphone', 'id': 'phone123'},
            {'name': 'Speaker', 'type': 'Speaker', 'id': 'speaker123'}
        ]
    }

    # sp.devices() をモックして上記のデータを返す
    with patch.object(spotify_handler.sp, 'devices', return_value=mock_devices):
        device_id = spotify_handler.get_available_device_id()
        assert device_id == 'phone123'  # スマートフォンが選ばれることを確認

def test_get_available_device_id_without_smartphone(spotify_handler):
    """スマートフォンデバイスが見つからない場合のテスト"""
    # モックデータ
    mock_devices = {
        'devices': [
            {'name': 'PC', 'type': 'Computer', 'id': 'pc123'},
            {'name': 'Speaker', 'type': 'Speaker', 'id': 'speaker123'}
        ]
    }

    # sp.devices() をモックして上記のデータを返す
    with patch.object(spotify_handler.sp, 'devices', return_value=mock_devices):
        device_id = spotify_handler.get_available_device_id()
        assert device_id is None  # スマートフォンが見つからないのでNoneが返る

def test_get_available_device_id_no_devices(spotify_handler):
    """デバイスが存在しない場合のテスト"""
    # モックデータ（デバイスなし）
    mock_devices = {'devices': []}

    # sp.devices() をモックして上記のデータを返す
    with patch.object(spotify_handler.sp, 'devices', return_value=mock_devices):
        device_id = spotify_handler.get_available_device_id()
        assert device_id is None  # デバイスがないのでNoneが返る
