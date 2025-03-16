import typer
from rich.console import Console
from claii.ai import chat
import subprocess

console = Console()
app = typer.Typer()

@app.command()
def gen(text: str, tool: str = "auto", run: bool = False):
    """Send a message to AI"""
    reply = chat(text, tool)
    if reply:
        console.print(f"[cyan]AI:[/cyan] {reply}")
    
    if run:
        try:
            console.print("[green]Executing command...[/green]")
            subprocess.run(reply, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error running command:[/red] {e}")
