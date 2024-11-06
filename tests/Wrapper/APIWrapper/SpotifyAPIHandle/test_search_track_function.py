import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pytest
import os
import sys
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
    sample2関数が200を返すようする。
    """
    status_code = 200
    track_id = "https://hogehoge.com"
    mocker.patch("handler.play_track", return_value=status_code)
    assert handler.play_track(track_id) == status_code