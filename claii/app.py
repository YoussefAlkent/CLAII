import typer
from rich.console import Console
from claii.commands import chat, config, tools, system

console = Console()
app = typer.Typer()

# Register CLI commands from different files
app.add_typer(chat.app, name="chat")
app.add_typer(config.app, name="config")
app.add_typer(tools.app, name="tools")
app.add_typer(system.app, name="system")
app.command()(chat.gen)

if __name__ == "__main__":
    app()
