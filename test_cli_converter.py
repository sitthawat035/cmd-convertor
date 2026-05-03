import os
import pytest
from unittest.mock import patch, MagicMock

# Import modules from refactored package
from core import CLIConverter, MiniMaxAPIError
from utils import is_exit_command

# ============================================================================
# Unit Tests for Utility Functions
# ============================================================================

def test_is_exit_command():
    assert is_exit_command("exit") == True
    assert is_exit_command("QUIT") == True
    assert is_exit_command("q") == True
    assert is_exit_command(" ออก ") == True
    assert is_exit_command("จบ") == True
    
    assert is_exit_command("hello") == False
    assert is_exit_command("ls") == False
    assert is_exit_command("clear") == False

# ============================================================================
# Unit Tests for CLIConverter Class
# ============================================================================

@pytest.fixture
def converter():
    """Fixture สำหรับสร้าง instance ของ CLIConverter"""
    return CLIConverter(
        api_key="test_api_key",
        base_url="https://test.api.endpoint",
        model="Test-Model"
    )

def test_validate_command(converter):
    # Valid commands
    assert converter._validate_command("ls -la") == True
    assert converter._validate_command("dir") == True
    assert converter._validate_command("  cd ..  ") == True
    
    # Invalid commands
    assert converter._validate_command("") == False
    assert converter._validate_command(" ") == False
    assert converter._validate_command("a") == False  # Length < 2

def test_build_payload(converter):
    payload = converter._build_payload("ls")
    
    assert payload["model"] == "Test-Model"
    assert len(payload["messages"]) == 2
    assert payload["messages"][0]["role"] == "system"
    assert payload["messages"][1]["role"] == "user"
    assert "แปลงคำสั่งนี้: ls" in payload["messages"][1]["content"]

@patch("core.requests.post")
def test_convert_success(mock_post, converter):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "Mocked AI Response"
                }
            }
        ]
    }
    mock_post.return_value = mock_response

    # Execute
    result = converter.convert("ls")

    # Assert
    assert result == "Mocked AI Response"
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs["headers"]["Authorization"] == "Bearer test_api_key"
    assert kwargs["json"]["model"] == "Test-Model"

@patch("core.requests.post")
def test_convert_invalid_command(mock_post, converter):
    result = converter.convert("")
    assert "❌ คำสั่งไม่ถูกต้อง" in result
    mock_post.assert_not_called()

@patch("core.requests.post")
def test_convert_connection_error(mock_post, converter):
    from requests.exceptions import ConnectionError
    mock_post.side_effect = ConnectionError("Connection failed")
    
    with pytest.raises(MiniMaxAPIError) as excinfo:
        converter.convert("ls")
    
    assert "ไม่สามารถเชื่อมต่อกับ API ได้" in str(excinfo.value)
