from claii.config import load_config
from claii.history import log_history
from claii.utils import is_openai_configured
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from claii.prompts.concise import build_prompt
from claii.utils import is_gemini_configured




def chat_gemini(message: str):
    """Chat with Gemini API using LangChain"""
    config = load_config()

    if not is_gemini_configured():
        return("[red]Gemini API key not set! Use `claii config set key gemini <your_key>`[/red]")

    api_key = config.get("gemini_api_key")
    model = config.get("gemini_model", "gemini-pro")
    llm = ChatGoogleGenerativeAI(api_key=api_key, model=model)
    formatted_prompt = build_prompt(message)
    reply = llm.invoke([HumanMessage(content=formatted_prompt)]).content.strip()
    log_history(message, reply)
    return reply
