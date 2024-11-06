import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pytest
import os
import sys
from unittest.mock import MagicMock
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from  src.Wrapper.APIWrapper.spotify_web_api_handler import * #テストするファイルを参照
from unittest.mock import MagicMock

#インスタンスを作成
spotify_handler = SpotifyWebAPIHandler()

def test_search_track(mocker):
    """
    search_trackメソッドをモックしてテストする
    """
    # モック用のクエリ
    query = "sample song"
    
    # モックで返す検索結果のデータを定義
    mock_search_result = {
        'tracks': {
            'items': [
                {
                    'id': 'mock_track_id',
                    'name': 'Mock Track Name'
                }
            ]
        }
    }
    
    # Spotifyのsearchメソッドをモックして、モックデータを返すように設定
    mocker.patch.object(spotify_handler.sp, "search", return_value=mock_search_result)
    
    # search_trackメソッドを実行し、結果を取得
    result = spotify_handler.search_track(query)
    
    # 結果が期待通りか確認
    assert result == {'id': 'mock_track_id', 'name': 'Mock Track Name'}
    assert result == {}