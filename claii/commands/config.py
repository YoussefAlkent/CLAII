import typer
from rich.console import Console
from claii.config import save_config, load_config

console = Console()
app = typer.Typer()

@app.command()
def set_key(api_key: str):
    """DEPRECATED: Set OpenAI API Key"""
    config = load_config()
    config["openai_api_key"] = api_key
    save_config(config)
    console.print("[green]API key saved successfully![/green]")

@app.command()
def set_model(model: str = "mistral"):
    """DEPRECATED: Set default Ollama model"""
    config = load_config()
    config["ollama_model"] = model
    save_config(config)
    console.print(f"[green]Ollama model set to '{model}'[/green]")

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

@app.command()
def get():
    """Show current configuration"""
    config = load_config()
    console.print(f"[yellow]Current Configuration:[/yellow] {config}")

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