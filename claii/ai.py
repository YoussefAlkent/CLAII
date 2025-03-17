import json
from rich.console import Console
from langchain_openai import OpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from claii.config import load_config
from claii.history import log_history
import requests
from claii.models.openai import chat_openai
from claii.models.ollama import chat_ollama
from claii.models.mistral import chat_mistral
from claii.models.perplexity import chat_perplexity
from claii.models.gemini import chat_gemini
from claii.models.deepseek import chat_deepseek


console = Console()

def gen_reply(message: str, tool: str = "auto"):
    """Select AI tool dynamically and chat based on user preferences or system availability."""
    config = load_config()

    # Load models from config
    ollama_model = config.get("ollama_model", "mistral")
    openai_model = config.get("openai_model", "gpt-4")
    deepseek_model = config.get("deepseek_model", "deepseek-chat")
    perplexity_model = config.get("perplexity_model", "pplx-7b-chat")
    mistral_model = config.get("mistral_model", "mistral-medium")
    gemini_model = config.get("gemini_model", "gemini-pro")

    # AI model selection logic
    if tool == "ollama" or (tool == "auto"):
        console.print(f"[yellow]Using Ollama ({ollama_model})[/yellow]")
        return chat_ollama(message, ollama_model)
    
    elif tool == "openai" or (tool == "auto"):
        console.print(f"[yellow]Using OpenAI ({openai_model})[/yellow]")
        return chat_openai(message)
    
    elif tool == "deepseek" or tool == "auto":
        console.print(f"[yellow]Using DeepSeek ({deepseek_model})[/yellow]")
        return chat_deepseek(message)
    
    elif tool == "perplexity" or tool == "auto":
        console.print(f"[yellow]Using Perplexity ({perplexity_model})[/yellow]")
        return chat_perplexity(message)
    
    elif tool == "mistral" or tool == "auto":
        console.print(f"[yellow]Using Mistral ({mistral_model})[/yellow]")
        return chat_mistral(message)
    
    elif tool == "gemini" or tool == "auto":
        console.print(f"[yellow]Using Gemini ({gemini_model})[/yellow]")
        return chat_gemini(message)

    else:
        console.print("[red]No AI tools available or invalid selection![/red]")
        return None
