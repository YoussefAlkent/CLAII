import json
from rich.console import Console
from langchain_openai import OpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from claii.config import load_config
from claii.utils import is_ollama_installed, is_openai_configured 
from claii.history import log_history


SHORT_ANSWER_PROMPT = PromptTemplate(
    input_variables=["query"],
    template=(
        "You are a concise assistant. Answer the following query in as little words as possible. "
        "If the user asks for a command, return only the command itself without extra explanation. "
        "You should not include any english words in your response if possible. "
        "You must always use a posix compliant command. you can assume that the user has the necessary permissions to run the command. "
        "if the command requires a specific file, you can assume that the file exists. "
        "if the command requires a specific binary, instruct the user to install the necessary package. "
        "you must always return a command that is safe to run. "
        "you must always assume the user does not have any binaries installed. "
        "do not add any characters to the command that are not necessary. "
        "Query: {query}"
    ),
)


console = Console()

def chat_ollama(message: str, model: str):
    """Chat with a local Ollama model using LangChain"""
    llm = ChatOllama(model=model)
    formatted_prompt = SHORT_ANSWER_PROMPT.format(query=message)  # Apply prompt template
    response = llm.invoke(formatted_prompt)
    log_history(message, response.content.strip())
    return response.content.strip()

def chat_openai(message: str):
    """Chat with OpenAI API using LangChain"""
    config = load_config()
    api_key = config.get("openai_api_key")
    if not api_key:
        console.print("[red]API key not set! Use `ai set-key <your_key>`[/red]")
        return {}

    llm = OpenAI(api_key=api_key, model="gpt-4-turbo")
    formatted_prompt = SHORT_ANSWER_PROMPT.format(query=message)  # Apply prompt template
    reply = llm.invoke(formatted_prompt).content.strip()
    log_history(message, reply)
    return reply


def chat(message: str, tool: str = "auto"):
    """Select AI tool and chat"""
    config = load_config()
    ollama_model = config.get("ollama_model", "mistral")

    if tool == "ollama" or (tool == "auto" and is_ollama_installed()):
        console.print(f"[yellow]Using Ollama ({ollama_model})[/yellow]")
        return chat_ollama(message, ollama_model)
    elif tool == "openai" or (tool == "auto" and is_openai_configured()):
        console.print("[yellow]Using OpenAI API[/yellow]")
        return chat_openai(message)
    else:
        console.print("[red]No AI tools available![/red]")
        return None
