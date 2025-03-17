"""Hello World plugin for CLAII."""

from claii.plugins.base import CLAIIPlugin
import typer

class HelloPlugin(CLAIIPlugin):
    """A simple Hello World plugin for CLAII."""
    
    @property
    def name(self) -> str:
        return "hello"
    
    @property
    def description(self) -> str:
        return "A simple Hello World plugin for CLAII."
    
    def get_commands(self):
        """Return commands provided by this plugin."""
        return [{
            "name": "hello",
            "description": "Say hello",
            "handler": self.hello_command
        }]
    
    def hello_command(self):
        """Say hello."""
        typer_app = typer.Typer()
        
        @typer_app.command()
        def world(name: str = typer.Option("World", help="Name to greet")):
            """Say hello to someone."""
            typer.echo(f"Hello, {name}!")
        
        return typer_app 