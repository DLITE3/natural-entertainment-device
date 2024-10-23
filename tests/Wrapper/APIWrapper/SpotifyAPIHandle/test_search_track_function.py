import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pytest
import os
import sys
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../APIWrapper')))
from  src.Wrapper.APIWrapper.spotify_web_api_handler import * #テストするファイルを参照

#インスタンスを作成
handler = SpotifyWebAPIHandler()
client_id = handler.get_client_id()
client_secret= handler.get_client_secret()

	
def test_search_track_function():
    assert handler.search_track_function() == 0