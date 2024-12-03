import pytest
from unittest.mock import patch
import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from src.Wrapper.APIWrapper.openai_api_handler import OpenAIAPIHandler

@patch("src.Wrapper.APIWrapper.openai_api_handler.OpenAIAPIHandler.post_request")  # requests.post をモックする
def test_post_request(mock_post):
    # モックレスポンスを設定
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.text =  "これはモックのレスポンスです"

    # テスト対象のクラスをインスタンス化
    handler = OpenAIAPIHandler()
    query = "特徴量のサンプルクエリ"
    
    # post_request を呼び出し
    response = handler.post_request(query)

    # モックが期待通りに呼び出されたか確認
    mock_post.assert_called_once_with(
        handler.api_url,  # 環境変数から設定されたURL
        json={
            "query": query,
            
        }
    )

    # レスポンス内容の検証
    assert response.status_code == 200
    assert response.text() == {"response": "これはモックのレスポンスです"}
    
