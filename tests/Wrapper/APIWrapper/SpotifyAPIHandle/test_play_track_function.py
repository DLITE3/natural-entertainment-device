import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pytest
import os
import sys
from unittest.mock import  MagicMock
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from  src.Wrapper.APIWrapper.spotify_web_api_handler import * #テストするファイルを参照
import requests

# インスタンスを作成
spotify_handler = SpotifyWebAPIHandler()

def test_play_track(mocker):
    """
    play_trackメソッドをモックしてテストする
    """
    # モック用のトラックID
    track_id = "sample_track_id"
    
    # get_available_device_idをモックし、有効なデバイスIDを返すようにする
    mocker.patch.object(spotify_handler, "get_available_device_id", return_value="mock_device_id")
    
    # start_playbackをモックして、Spotify APIに実際のリクエストを送らないようにする
    mock_start_playback = mocker.patch.object(spotify_handler.sp, "start_playback", return_value=None)
    
    # play_trackメソッドを実行
    spotify_handler.play_track(track_id)
    
    # start_playbackが正しいパラメータで呼び出されたかを確認
    mock_start_playback.assert_called_once_with(device_id="mock_device_id", uris=[f"spotify:track:{track_id}"])