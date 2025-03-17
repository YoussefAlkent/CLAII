import typer
import subprocess
from rich.console import Console
from rich.table import Table
from claii.plugins.manager import plugin_manager

console = Console()
app = typer.Typer()

@app.command()
def check():
    """Check if system meets requirements"""
    console.print("[yellow]Checking system dependencies...[/yellow]")
    subprocess.run(["python3", "--version"])

@app.command()
def version():
    """Display CLAII version."""
    console.print("[bold green]CLAII v0.1.0[/bold green]")

@app.command("list-plugins")
def list_plugins():
    """List all available plugins."""
    available_plugins = plugin_manager.get_available_plugin_names()
    enabled_plugins = plugin_manager.config["plugins"]["enabled"]
    
    table = Table(title="Available Plugins")
    table.add_column("Name", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Description", style="yellow")
    
    for plugin_name in available_plugins:
        plugin_instance = plugin_manager.get_plugin(plugin_name)
        status = "[green]Enabled[/green]" if plugin_name in enabled_plugins else "[red]Disabled[/red]"
        description = plugin_instance.description if plugin_instance else "Not loaded"
        table.add_row(str(plugin_name), status, description)
    
    console.print(table)

@app.command("enable-plugin")
def enable_plugin(name: str):
    """Enable a plugin."""
    if plugin_manager.enable_plugin(name):
        console.print(f"[green]Plugin '{name}' enabled successfully[/green]")
    else:
        console.print(f"[red]Failed to enable plugin '{name}'[/red]")

@app.command("disable-plugin")
def disable_plugin(name: str):
    """Disable a plugin."""
    if plugin_manager.disable_plugin(name):
        console.print(f"[green]Plugin '{name}' disabled successfully[/green]")
    else:
        console.print(f"[red]Failed to disable plugin '{name}'[/red]")

