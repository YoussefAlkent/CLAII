import typer
import subprocess
from rich.console import Console

console = Console()
app = typer.Typer()

@app.command()
def check():
    """Check if system meets requirements"""
    console.print("[yellow]Checking system dependencies...[/yellow]")
    subprocess.run(["python3", "--version"])

