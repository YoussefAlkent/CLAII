from claii.config import load_config
from claii.history import log_history
# from claii.utils import is_ollama_installed, is_openai_configured
from claii.prompts.concise import SHORT_ANSWER_PROMPT
import requests
from claii.utils import is_deepseek_configured


def chat_deepseek(message: str):
    """Chat with DeepSeek API using direct API call"""
    config = load_config()

    if not is_deepseek_configured():
        return("[red]DeepSeek API key not set! Use `claii config set key deepseek <your_key>`[/red]")

    api_key = config.get("deepseek_api_key")
    model = config.get("deepseek_model", "deepseek-chat")
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": SHORT_ANSWER_PROMPT.format(query=message)}]
    }

    response = requests.post(url, json=payload, headers=headers)
    reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    log_history(message, reply)
    return reply

