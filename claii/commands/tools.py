import typer
from rich.console import Console
from claii.utils import is_ollama_installed, is_openai_configured

console = Console()
app = typer.Typer()

@app.command()
def list():
    """List available AI tools"""
    console.print("[bold yellow]AI Tools Detection:[/bold yellow]")
    console.print(f"🔹 Ollama Installed: {'✅ Yes' if is_ollama_installed() else '❌ No'}")
    console.print(f"🔹 OpenAI Configured: {'✅ Yes' if is_openai_configured() else '❌ No'}")

    if not is_ollama_installed() and not is_openai_configured():
        console.print("[red]No AI tools detected![/red]")
