import os
import subprocess
from rich.console import Console
import typer

console = Console()
app = typer.Typer()

HISTORY_PATH = os.path.expanduser("~/.ai-cli-history.log")

@app.command()
def history():
    """Show previous AI conversations"""
    if not os.path.exists(HISTORY_PATH):
        console.print("[yellow]No history found.[/yellow]")
        return
    with open(HISTORY_PATH, "r") as f:
        console.print(f.read())
