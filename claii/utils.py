import os

def is_ollama_installed():
    """Check if Ollama is installed"""
    return os.system("which ollama > /dev/null 2>&1") == 0

def is_openai_configured():
    """Check if OpenAI API key is set"""
    from claii.config import load_config
    config = load_config()
    return bool(config.get("openai_api_key"))
