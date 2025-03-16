#!/usr/bin/env python3

from asyncio.log import logger
import typer
import os
import json
import subprocess
from rich.console import Console
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

console = Console()
app = typer.Typer()

CONFIG_DIR = os.path.expanduser("~/.config/CLAII/")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
HISTORY_PATH = os.path.expanduser("~/.ai-cli-history.log")


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

def ensure_config_dir():
    """Ensure that the configuration directory exists."""
    os.makedirs(CONFIG_DIR, exist_ok=True)

def load_config():
    """Load configuration file"""
    ensure_config_dir()
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    """Save configuration to file"""
    ensure_config_dir()
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def is_ollama_installed():
    """Check if Ollama is installed"""
    return os.system("which ollama > /dev/null 2>&1") == 0

def is_openai_configured():
    """Check if OpenAI API key is set"""
    config = load_config()
    return bool(config.get("openai_api_key"))

def log_history(message: str, reply: str):
    """Log the AI conversation to a history file"""
    with open(HISTORY_PATH, "a") as f:
        f.write(f"Q: {message}\nA: {reply}\n---\n")

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
    formatted_prompt = SHORT_ANSWER_PROMPT.format(query=message)  # Apply prompt template
    response = llm.invoke(formatted_prompt)
    return response.content.strip()


def chat_openai(message: str):
    """Chat with OpenAI API using LangChain"""
    config = load_config()
    api_key = config.get("openai_api_key")
    if not api_key:
        console.print("[red]API key not set! Use `ai set-key <your_key>`[/red]")
        raise typer.Exit()

    llm = OpenAI(api_key=api_key, model="gpt-4-turbo")
    formatted_prompt = SHORT_ANSWER_PROMPT.format(query=message)  # Apply prompt template
    return llm.invoke(formatted_prompt).content.strip()

@app.command()
def set_default_tool(tool: str):
    """Set the default AI tool (ollama or openai)"""
    if tool not in ["ollama", "openai"]:
        console.print("[red]Invalid option! Choose either 'ollama' or 'openai'.[/red]")
        raise typer.Exit()

    config = load_config()
    config["default_tool"] = tool
    save_config(config)
    console.print(f"[green]Default AI tool set to '{tool}'[/green]")

@app.command()
def get(param: str):
    """Retrieve configuration values (key, model, tool)"""
    valid_params = ["key", "model", "tool", "all"]
    if param not in valid_params:
        console.print(f"[red]Invalid parameter! Choose from {', '.join(valid_params)}[/red]")
        raise typer.Exit()

    config = load_config()

    if param == "key":
        console.print(f"[yellow]OpenAI API Key:[/yellow] {'✅ Set' if config.get('openai_api_key') else '❌ Not Set'}")

    elif param == "model":
        console.print(f"[yellow]Ollama Model:[/yellow] {config.get('ollama_model', 'mistral')}")

    elif param == "tool":
        console.print(f"[yellow]Default AI Tool:[/yellow] {config.get('default_tool', 'auto')}")

    elif param == "all":
        console.print("\n[bold yellow]Current Configuration:[/bold yellow]")
        console.print(f"🔹 OpenAI API Key: {'✅ Set' if config.get('openai_api_key') else '❌ Not Set'}")
        console.print(f"🔹 Ollama Model: {config.get('ollama_model', 'mistral')}")
        console.print(f"🔹 Default AI Tool: {config.get('default_tool', 'auto')}")


@app.command()
def set(param: str, value: str):
    """Set various configuration options (key, model, tool)"""
    valid_params = ["key", "model", "tool"]

    if param not in valid_params:
        console.print(f"[red]Invalid parameter! Choose from {', '.join(valid_params)}[/red]")
        raise typer.Exit()

    config = load_config()

    if param == "key":
        config["openai_api_key"] = value
        console.print("[green]OpenAI API key set successfully![/green]")

    elif param == "model":
        config["ollama_model"] = value
        console.print(f"[green]Ollama model set to '{value}'[/green]")

    elif param == "tool":
        if value not in ["ollama", "openai"]:
            console.print("[red]Invalid option! Choose either 'ollama' or 'openai'.[/red]")
            raise typer.Exit()
        config["default_tool"] = value
        console.print(f"[green]Default AI tool set to '{value}'[/green]")

    save_config(config)

@app.command()
def chat(message: str, tool: str = 'ollama', run: bool = False):
    """Send message to AI (auto-detect tool, or choose OpenAI/Ollama)"""
    config = load_config()
    ollama_model = config.get("ollama_model", "mistral")
    default_tool = config.get("default_tool", "ollama") 

    tool = tool or default_tool
    if tool == "ollama" and is_ollama_installed():
        console.print(f"[yellow]Using Ollama ({ollama_model})[/yellow]")
        reply = chat_ollama(message, ollama_model)
    elif tool == "openai" and is_openai_configured():
        console.print("[yellow]Using OpenAI API[/yellow]")
        reply = chat_openai(message)
    else:
        console.print("[red]No available AI tools! Install Ollama or set an OpenAI API key.[/red]")
        return

    if reply:
        console.print(f"[cyan]AI:[/cyan] {reply}")
        log_history(message, reply)
    
    if run:
        try:
            console.print("[green]Executing command...[/green]")
            subprocess.run(reply, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error running command:[/red] {e}")

@app.command()
def history():
    """Show previous AI conversations"""
    if not os.path.exists(HISTORY_PATH):
        console.print("[yellow]No history found.[/yellow]")
        return
    with open(HISTORY_PATH, "r") as f:
        console.print(f.read())




if __name__ == "__main__":
    app()
