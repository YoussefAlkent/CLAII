import os
import subprocess
from claii.config import load_config


def is_ollama_installed():
    """Check if Ollama is installed"""
    return os.system("which ollama > /dev/null 2>&1") == 0

def is_openai_configured():
    """Check if OpenAI API key is set"""
    config = load_config()
    return bool(config.get("openai_api_key"))

def is_deepseek_configured():
    """Check if DeepSeek API key is set."""
    config = load_config()
    return bool(config.get("deepseek_api_key"))

def is_perplexity_configured():
    """Check if Perplexity API key is set."""
    config = load_config()
    return bool(config.get("perplexity_api_key"))

def is_mistral_configured():
    """Check if Mistral API key is set."""
    config = load_config()
    return bool(config.get("mistral_api_key"))

def is_gemini_configured():
    """Check if Gemini API key is set."""
    config = load_config()
    return bool(config.get("gemini_api_key"))

def is_ollama_running():
    """Check if Ollama is running."""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False  # Ollama binary not found