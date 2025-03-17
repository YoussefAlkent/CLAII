import pytest
from claii.ai import gen_reply
from claii.utils import is_openai_configured
from claii.models.openai import chat_openai

@pytest.mark.parametrize("tool", ["ollama", "openai", "deepseek", "perplexity", "mistral", "gemini"])
def test_chat_model_selection(mocker, tool):
    """Test AI model selection logic"""
    mocker.patch("claii.config.load_config", return_value={"tool":tool})
    mock_chat_function = mocker.patch(f"claii.models.{tool}.chat_{tool}", return_value="Mocked response")
    response = gen_reply("Hello world in bash", tool)
    assert response == "API key not set!"
    mock_chat_function.assert_called_once()

def test_chat_openai_api_key_missing(mocker):
    """Test OpenAI API when API key is missing"""
    mocker.patch("claii.config.load_config", return_value={})
    response = chat_openai("Hello world in Bash")
    assert "API key not set" in response
