import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pytest
import os
import sys
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from  src.Wrapper.APIWrapper.spotify_web_api_handler import * #テストするファイルを参照

#インスタンスを作成
handler = SpotifyWebAPIHandler()
client_id = handler.get_client_id()
client_secret= handler.get_client_secret()
	
 
def test_get_apotify_api_mock_200(mocker):
    """
    関数がsuccessを返すようする。
    """
    status_code = "success"
    self = "you"
    mocker.patch("src.Wrapper.APIWrapper.spotify_web_api_handler", return_value=status_code)
    assert handler.connected_to_spotify_web_api(  ) == status_code

def test_get_apotify_api_mock_404(mocker):
    """
    関数がfailureを返すようする。
    """
    status_code = "failure"
    self = "who"
    mocker.patch("src.Wrapper.APIWrapper.spotify_web_api_handler", return_value=status_code)
    assert handler.connected_to_spotify_web_api( ) == status_code