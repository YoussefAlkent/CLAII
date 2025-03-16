import pytest
from claii.models.ollama import chat_ollama

def test_chat_ollama_not_running(mocker):
    """Test Ollama when its not running"""
    mocker.patch("claii.utils.is_ollama_installed", return_value=True)
    mocker.patch("langchain_ollama.ChatOllama.invoke", side_effect=ConnectionError("Ollama is not running"))
    response = chat_ollama("Hello world in bash", "qwen2.5-coder:1.5b")
    assert "Ollama is not running" in response