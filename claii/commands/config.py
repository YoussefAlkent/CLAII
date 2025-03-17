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
def set(param: str, provider: str, value: str):
    """Set various configuration options (API keys, models, tools)"""
    
    # Handle plugin settings
    if param.startswith("plugins."):
        config = load_config()
        
        # Special case for plugins.settings.plugin_name format
        if param.startswith("plugins.settings."):
            parts = param.split(".")
            if len(parts) == 3:  # plugins.settings.pluginname
                plugin_name = parts[2]
                
                # Make sure plugins and settings structure exists
                if "plugins" not in config:
                    config["plugins"] = {}
                if "settings" not in config["plugins"]:
                    config["plugins"]["settings"] = {}
                
                # Convert string settings to dict if needed
                if plugin_name in config["plugins"]["settings"] and not isinstance(config["plugins"]["settings"][plugin_name], dict):
                    # We have a string value where we expect a dict, fix it
                    old_value = config["plugins"]["settings"][plugin_name]
                    config["plugins"]["settings"][plugin_name] = {}
                
                # Initialize plugin settings dict if needed
                if plugin_name not in config["plugins"]["settings"]:
                    config["plugins"]["settings"][plugin_name] = {}
                
                # Set the value in the plugin settings
                config["plugins"]["settings"][plugin_name][provider] = value
                
                save_config(config)
                console.print(f"[green]Plugin config '{plugin_name}.{provider}' set to '{value}'[/green]")
                return
        
        # Handle other plugin paths
        parts = param.split(".")
        current = config
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = value
        save_config(config)
        console.print(f"[green]Config '{param}' set to '{value}'[/green]")
        return
    
    # Handle regular settings
    valid_params = ["key", "model", "tool"]
    valid_providers = ["openai", "deepseek", "perplexity", "mistral", "gemini", "ollama"]

    if param not in valid_params:
        console.print(f"[red]Invalid parameter! Choose from {', '.join(valid_params)}[/red]")
        raise typer.Exit()

    if provider not in valid_providers:
        console.print(f"[red]Invalid provider! Choose from {', '.join(valid_providers)}[/red]")
        raise typer.Exit()
    
    if param == "key" and provider == "ollama":
        console.print("[red]Ollama API key is not required! Use `claii set model ollama <model>` instead[/red]")
        raise typer.Exit()

    config = load_config()

    if param == "key":
        config[f"{provider}_api_key"] = value
        console.print(f"[green]{provider.capitalize()} API key set successfully![/green]")

    elif param == "model":
        config[f"{provider}_model"] = value
        console.print(f"[green]{provider.capitalize()} model set to '{value}'[/green]")

    elif param == "tool":
        config["default_tool"] = provider
        console.print(f"[green]Default AI tool set to '{provider}'[/green]")

    else:
        console.print("[red]Invalid configuration option")
        raise typer.Exit()

    save_config(config)


@app.command("get-all")
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