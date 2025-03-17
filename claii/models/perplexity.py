from claii.config import load_config
from claii.history import log_history
from claii.utils import is_ollama_installed
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from claii.prompts.concise import build_prompt



def chat_perplexity(message: str):
    """Chat with Perplexity AI using LangChain's ChatAnthropic (Claude-based models)"""
    config = load_config()
    api_key = config.get("perplexity_api_key")
    model = config.get("perplexity_model", "pplx-7b-chat")

    if not api_key:
        return("[red]Perplexity API key not set! Use `claii config set key perplexity <your_key>`[/red]")

    llm = ChatAnthropic(api_key=api_key, model=model)
    formatted_prompt = build_prompt(message)
    reply = llm.invoke([HumanMessage(content=formatted_prompt)]).content.strip()
    log_history(message, reply)
    return reply

