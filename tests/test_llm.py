import pytest
from unittest.mock import MagicMock, patch
from src.llm.openai_provider import OpenAIProvider
from src.llm.anthropic_provider import AnthropicProvider

@patch("openai.OpenAI")
def test_openai_extraction(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='{"first_name": "Test"}'))],
        usage=MagicMock(total_tokens=100)
    )
    
    provider = OpenAIProvider()
    # Mock encode_image
    with patch.object(OpenAIProvider, "encode_image", return_value="base64"):
        result = provider.extract("dummy.jpg", "prompt", {})
        assert result == {"first_name": "Test"}

@patch("anthropic.Anthropic")
def test_anthropic_extraction(mock_anthropic):
    mock_client = MagicMock()
    mock_anthropic.return_value = mock_client
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text='{"first_name": "Test"}')],
        usage=MagicMock(input_tokens=50, output_tokens=50)
    )
    
    provider = AnthropicProvider()
    with patch.object(AnthropicProvider, "encode_image", return_value="base64"):
        result = provider.extract("dummy.jpg", "prompt", {})
        assert result == {"first_name": "Test"}
