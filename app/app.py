#!/usr/bin/env python3

from asyncio.log import logger
import typer
import os
import json
from rich.console import Console
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_ollama import ChatOllama

console = Console()
app = typer.Typer()

CONFIG_PATH = os.path.expanduser("~/.ai-cli-config.json")

def load_config():
    """Load configuration file"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def is_ollama_installed():
    """Check if Ollama is installed"""
    return os.system("which ollama > /dev/null 2>&1") == 0

def is_openai_configured():
    """Check if OpenAI API key is set"""
    config = load_config()
    return bool(config.get("openai_api_key"))

@app.command()
def tools():
    """List available AI tools"""
    ollama_installed = is_ollama_installed()
    openai_configured = is_openai_configured()

    console.print("[bold yellow]AI Tools Detection:[/bold yellow]")
    console.print(f"🔹 Ollama Installed: {'✅ Yes' if ollama_installed else '❌ No'}")
    console.print(f"🔹 OpenAI Configured: {'✅ Yes' if openai_configured else '❌ No'}")

    if not ollama_installed and not openai_configured:
        console.print("[red]No AI tools detected! Please install Ollama or set an OpenAI API key.[/red]")

@app.command()
def set_key(api_key: str):
    """Set OpenAI API key"""
    config = load_config()
    config["openai_api_key"] = api_key
    save_config(config)
    console.print("[green]API key saved successfully![/green]")

@app.command()
def set_model(model: str = "mistral"):
    """Set default Ollama model"""
    config = load_config()
    config["ollama_model"] = model
    save_config(config)
    console.print(f"[green]Ollama model set to '{model}'[/green]")

def chat_ollama(message: str, model: str):
    """Chat with a local Ollama model using LangChain"""
    llm = ChatOllama(model=model)
    response = llm.invoke(message)
    return response.content.strip()
    # content = response.get("content", "").strip()
    # if content:
    #     return content
    # else:
    #     logger.error("No response from Ollama!")
    #     return "I'm sorry, I couldn't understand that."

def chat_openai(message: str):
    """Chat with OpenAI API using LangChain"""
    config = load_config()
    api_key = config.get("openai_api_key")
    if not api_key:
        console.print("[red]API key not set! Use `ai set-key <your_key>`[/red]")
        raise typer.Exit()

    llm = OpenAI(api_key=api_key, model="gpt-4-turbo")
    return llm.invoke(message)

@app.command()
def chat(message: str, tool: str = "auto"):
    """Send message to AI (auto-detect tool, or choose OpenAI/Ollama)"""
    config = load_config()
    ollama_model = config.get("ollama_model", "mistral")

    if tool == "ollama" or (tool == "auto" and is_ollama_installed()):
        console.print(f"[yellow]Using Ollama ({ollama_model})[/yellow]")
        reply = chat_ollama(message, ollama_model)
    elif tool == "openai" or (tool == "auto" and is_openai_configured()):
        console.print("[yellow]Using OpenAI API[/yellow]")
        reply = chat_openai(message)
    else:
        console.print("[red]No available AI tools! Install Ollama or set an OpenAI API key.[/red]")
        return

    if reply:
        console.print(f"[cyan]AI:[/cyan] {reply}")

if __name__ == "__main__":
    app()
