from claii.config import load_config
from claii.history import log_history
from claii.prompts.concise import build_prompt
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage
import requests
from claii.utils import is_deepseek_configured



def chat_deepseek(message: str):
    """Chat with Deepseek using Langchain"""
    config = load_config()

    if not is_deepseek_configured():
        return("[red]DeepSeek API key not set! Use `claii config set key deepseek <your_key>`[/red]")
    
    api_key = config.get("deepseek_api_key")
    model = config.get("deepseek_model", "deepseek-chat")
    llm = ChatDeepSeek(api_key=api_key, model=model)
    formatted_prompt = build_prompt(message)
    reply = llm.invoke([HumanMessage(content=formatted_prompt)]).content.strip()
    log_history(message, reply)
    return reply