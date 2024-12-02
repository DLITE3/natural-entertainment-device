import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
from PIL import Image
import os
import sys
import base64  # base64のインポートを追加
sys.path.append(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
# テストの冒頭でモックを適用
with patch.dict('sys.modules', {'RPi': MagicMock(), 'RPi.GPIO': MagicMock(),'picamera2': MagicMock(),'adafruit_rgb_display': MagicMock()}):
    from src.Wrapper.APIWrapper.stable_diffusion_api_wrapper import StableDiffusionWrapper
# 'picamera2'モジュールをモック
  



@pytest.fixture
def sd_wrapper():
    """StableDiffusionWrapperのインスタンスを返すfixture"""
    return StableDiffusionWrapper()

def test_api_url_not_set():
    """環境変数 STABLE_DIFFUSION_API_URL が設定されていない場合に例外が発生することを確認"""
    with patch.dict(os.environ, {"STABLE_DIFFUSION_API_URL": ""}):  # 環境変数を空に設定
        with pytest.raises(ValueError, match="STABLE_DIFFUSION_API_URL が設定されていません。"):
            StableDiffusionWrapper()

def test_base64_to_image_valid(sd_wrapper):
    """有効なBase64文字列から画像を生成できることを確認"""
    # ダミーのBase64文字列（白画像をエンコード）
    image = Image.new("RGB", (100, 100), color="white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    base64_string = base64.b64encode(buffer.getvalue()).decode("utf-8")

    result_image = sd_wrapper.base64_to_image(base64_string)

    assert isinstance(result_image, Image.Image)
    assert result_image.size == (100, 100)

def test_base64_to_image_invalid(sd_wrapper):
    """無効なBase64文字列を処理すると例外が発生することを確認"""
    invalid_base64 = "not_a_valid_base64"

    with pytest.raises(Exception):
        sd_wrapper.base64_to_image(invalid_base64)

@patch("src.Wrapper.APIWrapper.stable_diffusion_wrapper.requests.post")
def test_generate_image_success(mock_post, sd_wrapper):
    """APIが成功した場合に画像が返されることを確認"""
    # モックレスポンス
    mock_response = MagicMock()
    mock_image = Image.new("RGB", (100, 100), color="blue")
    buffer = BytesIO()
    mock_image.save(buffer, format="PNG")
    base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    mock_response.json.return_value = {"image": base64_image}
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    prompt = "A beautiful landscape with mountains"
    result_image = sd_wrapper.generate_image(prompt)

    assert isinstance(result_image, Image.Image)
    assert result_image.size == (100, 100)

@patch("src.Wrapper.APIWrapper.stable_diffusion_wrapper.requests.post")
def test_generate_image_no_image_data(mock_post, sd_wrapper):
    """APIレスポンスに画像データが含まれない場合"""
    # モックレスポンス
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    prompt = "A futuristic cityscape"
    with pytest.raises(ValueError, match="レスポンスに画像データが含まれていません。"):
        sd_wrapper.generate_image(prompt)

@patch("src.Wrapper.APIWrapper.stable_diffusion_wrapper.requests.post")
def test_generate_image_request_error(mock_post, sd_wrapper):
    """APIリクエストで例外が発生する場合"""
    mock_post.side_effect = Exception("Connection Error")

    prompt = "A sci-fi robot in a dystopian city"
    with pytest.raises(Exception, match="Connection Error"):
        sd_wrapper.generate_image(prompt)
