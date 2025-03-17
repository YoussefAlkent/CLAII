from claii.config import load_config
from claii.history import log_history
from claii.utils import is_openai_configured
from langchain_openai import OpenAI
from claii.prompts.concise import build_prompt

def chat_openai(message: str):
    """Chat with OpenAI API using LangChain"""
    config = load_config()
    api_key = config.get("openai_api_key")
    if not api_key:
        return("[red]API key not set! Use `ai set-key <your_key>`[/red]")

    llm = OpenAI(api_key=api_key, model="gpt-3.5-turbo-0125")
    formatted_prompt = build_prompt(message)  # Apply prompt template
    reply = llm.invoke(formatted_prompt).content.strip()
    log_history(message, reply)
    return reply
