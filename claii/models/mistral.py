from claii.config import load_config
from claii.history import log_history
from claii.utils import is_openai_configured
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage
from claii.prompts.concise import build_prompt
from claii.utils import is_mistral_configured


def chat_mistral(message: str):
    """Chat with Mistral API using LangChain"""
    config = load_config()

    if not is_mistral_configured():
        return("[red]Mistral API key not set! Use `claii config set key mistral <your_key>`[/red]")

    api_key = config.get("mistral_api_key")
    model = config.get("mistral_model", "mistral-medium")
    llm = ChatMistralAI(api_key=api_key, model=model)
    formatted_prompt = build_prompt(message)
    reply = llm.invoke([HumanMessage(content=formatted_prompt)]).content.strip()
    log_history(message, reply)
    return reply