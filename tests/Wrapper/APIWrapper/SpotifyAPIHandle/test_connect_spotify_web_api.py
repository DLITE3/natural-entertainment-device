import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pytest
import os
import sys
from unittest.mock import patch, MagicMock
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from src.Wrapper.APIWrapper.spotify_web_api_handler import *  # テストするファイルを参照


# SpotifyOAuthをモックするためのフィクスチャ
@pytest.fixture
def mock_spotify_oauth():
    with patch('src.Wrapper.APIWrapper.spotify_web_api_handler.SpotifyOAuth') as mock_oauth:
        yield mock_oauth


# トークン取得に失敗する場合のテスト
def test_initialize_auth_manager_with_failed_token_acquisition(mock_spotify_oauth):
    mock_auth_instance = MagicMock()
    mock_spotify_oauth.return_value = mock_auth_instance
    
    # 認証情報が無効で、トークン取得に失敗する場合
    mock_auth_instance.get_cached_token.return_value = None  # キャッシュされたトークンはない
    mock_auth_instance.get_access_token.side_effect = Exception("認証に失敗しました: 無効なクライアント情報")  # トークン取得が失敗する

    # SpotifyWebAPIHandlerのインスタンス作成時に例外が発生することを確認
    with pytest.raises(Exception, match="認証に失敗しました: 無効なクライアント情報"):
        handler = SpotifyWebAPIHandler()  # 例外が発生するので、この行は実行されません

    # SpotifyOAuthが呼ばれたか確認
    assert mock_spotify_oauth.called == True  # SpotifyOAuthが呼ばれたことを確認
    
    # get_access_token が試みられたかを確認
    assert mock_auth_instance.get_access_token.called == True  # トークン取得が試みられたことを確認

    # SpotifyWebAPIHandlerがインスタンス化されなかったことを確認
    # 例外が発生したので、handler変数は未定義のままであるべき
    try:
        assert handler is None  # handlerは定義されていないはず
    except UnboundLocalError:
        pass  # handlerが定義されていない場合、UnboundLocalErrorが発生するので、それを期待
