"""
Example Hello World Plugin for CLAII

This is a simple example plugin that adds a "hello" command to CLAII.
"""

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
    
    @property
    def version(self) -> str:
        return "0.1.0"
    
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
    
    def on_load(self):
        """Called when the plugin is loaded."""
        print(f"Plugin {self.name} loaded!")
    
    def on_unload(self):
        """Called when the plugin is unloaded."""
        print(f"Plugin {self.name} unloaded!") 