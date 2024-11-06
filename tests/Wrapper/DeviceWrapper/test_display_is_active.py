from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))
from src.Wrapper.DeviceWrapper import DisplayWrapper

def test_display_mock_connected_true():
    """
    is_connected関数の返す値がTrueになるようにする。
    """
    # ディスプレイオブジェクトをモック
    mock_display = DisplayWrapper()
    mock_display.connected = True

    # テスト実行
    assert mock_display.is_connected() == True

def test_display_mock_connected_false():
    """
    is_connected関数の返す値がFalseになるようにする。
    """
    # ディスプレイオブジェクトをモック
    mock_display = DisplayWrapper()
    mock_display.connected = False

    # テスト実行
    assert mock_display.is_connected() == False
