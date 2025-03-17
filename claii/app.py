import typer
from rich.console import Console
from claii.commands import config, generate, tools, system
from claii.plugins.manager import plugin_manager

console = Console()
app = typer.Typer()

# Register CLI commands from different files
# app.add_typer(chat.app, name="chat")
app.add_typer(config.app, name="config")
app.add_typer(tools.app, name="tools")
app.add_typer(system.app, name="system")
app.command()(generate.chat)

# Initialize plugin system
plugin_manager.load_plugins()

# Register plugin commands
for cmd_name, cmd_info in plugin_manager.commands.items():
    handler = plugin_manager.get_command_handler(cmd_name)
    if handler:
        app.add_typer(handler(), name=cmd_name)

if __name__ == "__main__":
    app()
