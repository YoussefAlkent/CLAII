from claii.config import load_config
from claii.history import log_history
from claii.utils import is_ollama_installed, is_ollama_running
from langchain_ollama import ChatOllama
from claii.prompts.concise import build_prompt



def chat_ollama(message: str, model: str):
    """Chat with a local Ollama model using LangChain"""
    if not is_ollama_installed():
        return("[red]Ollama is not installed![/red]")
    if not is_ollama_running():
        return("[red]Ollama is not running![/red]")
    llm = ChatOllama(model=model)
    formatted_prompt = build_prompt(message)  # Apply prompt template
    response = llm.invoke(formatted_prompt)
    log_history(message, response.content.strip())
    return response.content.strip()
