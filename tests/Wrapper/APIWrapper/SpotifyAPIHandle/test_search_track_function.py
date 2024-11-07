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

def test_search_track_found(spotify_handler):
    """指定した曲が見つかった場合のテスト"""
    # モックデータ（検索結果）
    mock_search_result = {
        'tracks': {
            'items': [
                {'id': 'track123', 'name': 'henceforthorange'}
            ]
        }
    }

    # sp.search() をモックして上記のデータを返す
    with patch.object(spotify_handler.sp, 'search', return_value=mock_search_result):
        track_info = spotify_handler.search_track("henceforthorange")
        assert track_info is not None  # トラック情報が返されることを確認
        assert track_info['id'] == 'track123'  # トラックIDが正しいことを確認
        assert track_info['name'] == 'henceforthorange'  # トラック名が正しいことを確認

def test_search_track_not_found(spotify_handler):
    """指定した曲が見つからなかった場合のテスト"""
    # モックデータ（検索結果なし）
    mock_search_result = {
        'tracks': {
            'items': []
        }
    }

    # sp.search() をモックして上記のデータを返す
    with patch.object(spotify_handler.sp, 'search', return_value=mock_search_result):
        track_info = spotify_handler.search_track("nonexistenttrack")
        assert track_info is None  # トラック情報が返されないことを確認
