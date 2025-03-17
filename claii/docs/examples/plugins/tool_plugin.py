"""
Example Tool Plugin for CLAII

This is an example plugin that adds utility tools to CLAII.
"""

from claii.plugins.base import CLAIIPlugin
import datetime
import platform
import psutil
import typer
from rich.console import Console
from rich.table import Table

console = Console()

class SystemInfoPlugin(CLAIIPlugin):
    """A plugin that provides system information tools."""
    
    @property
    def name(self) -> str:
        return "sysinfo"
    
    @property
    def description(self) -> str:
        return "Provides system information tools."
    
    @property
    def version(self) -> str:
        return "0.1.0"
    
    def get_commands(self):
        """Return commands provided by this plugin."""
        return [{
            "name": "sysinfo",
            "description": "Get system information",
            "handler": self.sysinfo_command
        }]
    
    def get_tools(self):
        """Return tools provided by this plugin."""
        return [{
            "name": "system_summary",
            "description": "Get system summary",
            "handler": self.system_summary_tool
        }, {
            "name": "current_time",
            "description": "Get current time",
            "handler": self.current_time_tool
        }]
    
    def sysinfo_command(self):
        """System information command."""
        typer_app = typer.Typer()
        
        @typer_app.command()
        def summary():
            """Show system summary."""
            info = self.system_summary_tool()
            
            table = Table(title="System Information")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="yellow")
            
            for key, value in info.items():
                table.add_row(key, str(value))
            
            console.print(table)
        
        @typer_app.command()
        def time():
            """Show current time."""
            time_info = self.current_time_tool()
            console.print(f"[cyan]Current time:[/cyan] [yellow]{time_info['formatted_time']}[/yellow]")
            console.print(f"[cyan]Timezone:[/cyan] [yellow]{time_info['timezone']}[/yellow]")
        
        return typer_app
    
    def system_summary_tool(self):
        """Get system summary information."""
        try:
            return {
                "OS": platform.system(),
                "OS Version": platform.version(),
                "Architecture": platform.machine(),
                "Processor": platform.processor(),
                "Python Version": platform.python_version(),
                "CPU Cores": psutil.cpu_count(logical=False),
                "Logical CPUs": psutil.cpu_count(logical=True),
                "Memory (GB)": round(psutil.virtual_memory().total / (1024**3), 2),
                "Memory Usage (%)": psutil.virtual_memory().percent,
                "Disk Usage (%)": psutil.disk_usage('/').percent
            }
        except Exception as e:
            return {"error": str(e)}
    
    def current_time_tool(self):
        """Get current time information."""
        now = datetime.datetime.now()
        return {
            "timestamp": now.timestamp(),
            "formatted_time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "timezone": datetime.datetime.now().astimezone().tzinfo
        } 