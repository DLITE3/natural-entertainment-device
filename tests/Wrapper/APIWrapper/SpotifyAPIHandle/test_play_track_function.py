import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pytest
import os
import sys
from unittest.mock import patch, MagicMock
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from  src.Wrapper.APIWrapper.spotify_web_api_handler import * #テストするファイルを参照


@pytest.fixture
def spotify_handler():
    """SpotifyWebAPIHandlerのインスタンスを返すfixture"""
    return SpotifyWebAPIHandler()

def test_play_track_success(spotify_handler):
    """トラックが正常に再生される場合のテスト"""
    
    # モックデバイス情報（デバイスが1つ）
    mock_devices = {
        'devices': [
            {'name': 'Smartphone', 'type': 'Smartphone', 'id': 'device_id_123'}
        ]
    }

    # モック検索結果（指定した曲が存在する場合）
    mock_search_result = {
        'tracks': {
            'items': [
                {'id': 'track_id_123', 'name': 'Test Song'}
            ]
        }
    }

    # モックして、devicesとsearchを返す
    with patch.object(spotify_handler.sp, 'devices', return_value=mock_devices), \
         patch.object(spotify_handler.sp, 'search', return_value=mock_search_result), \
         patch.object(spotify_handler.sp, 'start_playback') as mock_start_playback:

        # 検索した曲を取得
        track_info = spotify_handler.search_track("Test Song")
        assert track_info != None  # トラック情報が返されることを確認

        # play_trackを呼び出して再生を開始
        result = spotify_handler.play_track(track_info['id'])

        # play_trackが正常に終了した場合、200を返すことを確認
        assert result == 200  # 正常終了した場合の戻り値

        # start_playbackが正しい引数で呼ばれたかを確認
        mock_start_playback.assert_called_once_with(
            device_id='device_id_123', uris=['spotify:track:track_id_123']
        )

def test_play_track_no_device(spotify_handler):
    """再生するデバイスが見つからない場合のテスト"""
    
    # モックデバイス情報（デバイスなし）
    mock_devices = {'devices': []}
    
    # モックして、devicesを返す
    with patch.object(spotify_handler.sp, 'devices', return_value=mock_devices), \
         patch.object(spotify_handler.sp, 'start_playback') as mock_start_playback:

        # 曲を検索
        track_info = spotify_handler.search_track("Test Song")
        
        # デバイスがない場合、再生しないことを確認
        result = spotify_handler.play_track(track_info['id'] if track_info else None)

        # 再生できるデバイスがない場合、戻り値はNoneになることを確認
        assert result == None  # 再生できなかった場合はNoneを返す

        mock_start_playback.assert_not_called()  # start_playbackが呼ばれていないことを確認

def test_play_track_search_failure(spotify_handler):
    """曲の検索に失敗した場合のテスト"""
    
    # モック検索結果（曲が見つからない場合）
    mock_search_result = {
        'tracks': {
            'items': []
        }
    }

    # モックして、検索結果なしを返す
    with patch.object(spotify_handler.sp, 'search', return_value=mock_search_result), \
         patch.object(spotify_handler.sp, 'start_playback') as mock_start_playback:

        # 曲が見つからない場合、プレイを試みても何もしないことを確認
        track_info = spotify_handler.search_track("Nonexistent Song")
        assert track_info == None  # トラック情報が返されないことを確認
        
        # 曲がないので再生は呼ばれない
        result = spotify_handler.play_track(track_info['id'] if track_info else None)
        assert result == None  # 検索失敗のため、再生できないことを確認

        mock_start_playback.assert_not_called()  # start_playbackが呼ばれていないことを確認

def test_play_track_auth_error(spotify_handler):
    """認証エラーが発生した場合のテスト"""
    
    # モックデバイス情報（デバイスが1つ）
    mock_devices = {
        'devices': [
            {'name': 'Smartphone', 'type': 'Smartphone', 'id': 'device_id_123'}
        ]
    }

    # モック検索結果（曲が見つかる）
    mock_search_result = {
        'tracks': {
            'items': [
                {'id': 'track_id_123', 'name': 'Test Song'}
            ]
        }
    }

    # 401エラーを発生させる
    with patch.object(spotify_handler.sp, 'devices', return_value=mock_devices), \
         patch.object(spotify_handler.sp, 'search', return_value=mock_search_result), \
          patch.object(spotify_handler.sp, 'start_playback', side_effect=spotipy.exceptions.SpotifyException(
             http_status=401, code='invalid_token', msg='Token expired')):

        # 曲を検索
        track_info = spotify_handler.search_track("Test Song")
        assert track_info != None  # トラック情報が返されることを確認

        # 認証エラーが発生するため、ステータスコード401が返ることを確認
        result = spotify_handler.play_track(track_info['id'])
        assert result == None  # 認証エラーのため、再生できないことを確認