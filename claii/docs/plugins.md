# CLAII Plugin System Documentation

## Overview

The CLAII Plugin System allows you to extend the functionality of CLAII with custom commands, AI models, and tools. This document provides a comprehensive guide to creating, installing, and managing plugins.

## Plugin Types

CLAII plugins can extend the application in three main ways:

1. **Commands**: Add new CLI commands to CLAII
2. **Models**: Add new AI models for chat completion
3. **Tools**: Add utility functions that can be used by other components

A single plugin can provide one or more of these extensions.

## Plugin Structure

Each plugin is a Python package with the following structure:

```
my_plugin/
  __init__.py  # Main plugin file with CLAIIPlugin class
  ... other files ...
```

The `__init__.py` file must contain a class that inherits from `CLAIIPlugin` and implements the required methods.

## Creating a Plugin

### Basic Plugin Template

Here's a template for creating a basic plugin:

```python
from claii.plugins.base import CLAIIPlugin

class MyPlugin(CLAIIPlugin):
    """Description of your plugin."""
    
    @property
    def name(self) -> str:
        """The unique name of the plugin."""
        return "my_plugin"
    
    @property
    def description(self) -> str:
        """A short description of the plugin."""
        return "My awesome CLAII plugin"
    
    @property
    def version(self) -> str:
        """The version of the plugin."""
        return "0.1.0"
    
    @property
    def config_schema(self):
        """Schema for plugin configuration."""
        return {
            "setting_name": {
                "type": "string",
                "default": "default_value",
                "description": "Description of the setting"
            }
        }
    
    def initialize(self, config):
        """Initialize the plugin with its configuration."""
        self.config = config
    
    def on_load(self):
        """Called when the plugin is loaded."""
        pass
    
    def on_unload(self):
        """Called when the plugin is unloaded."""
        pass
```

### Adding Commands

To add CLI commands to CLAII, implement the `get_commands` method:

```python
import typer

def get_commands(self):
    """Return list of commands provided by this plugin."""
    return [{
        "name": "my_command",
        "description": "Description of the command",
        "handler": self.my_command_handler
    }]

def my_command_handler(self):
    """Handler for the command."""
    app = typer.Typer()
    
    @app.command()
    def subcommand(param: str = typer.Option("default", help="Parameter description")):
        """Subcommand description."""
        typer.echo(f"Executing subcommand with {param}")
    
    return app
```

This will create a command that can be used like:

```
claii my_command subcommand --param value
```

### Adding AI Models

To add AI models to CLAII, implement the `get_models` method:

```python
def get_models(self):
    """Return list of AI models provided by this plugin."""
    return [{
        "name": "my_model",
        "description": "Description of the AI model",
        "handler": self.my_model_handler
    }]

def my_model_handler(self, message: str):
    """Handler for the AI model."""
    # Implement model-specific logic here
    # Must return a string response
    return f"Response to: {message}"
```

The model can then be used with:

```
claii chat "Your message" --tool my_model
```

### Adding Tools

To add utility tools to CLAII, implement the `get_tools` method:

```python
def get_tools(self):
    """Return list of tools provided by this plugin."""
    return [{
        "name": "my_tool",
        "description": "Description of the tool",
        "handler": self.my_tool_handler
    }]

def my_tool_handler(self, *args, **kwargs):
    """Handler for the tool."""
    # Implement tool-specific logic here
    return "Tool result"
```

## Plugin Configuration

Plugins can define their configuration schema using the `config_schema` property. This schema defines what settings are available, their types, default values, and descriptions.

Users can configure plugins using:

```
claii config set plugins.settings.<plugin_name> <setting_name> <value>
```

For example:

```
claii config set plugins.settings.my_plugin api_key abc123
```

Inside your plugin, you can access these settings through `self.config`:

```python
def my_method(self):
    api_key = self.config.get("api_key")
    # Use the API key...
```

## Installing Plugins

Plugins can be installed in one of these locations:

1. **Built-in plugins**: `claii/plugins/builtin/<plugin_name>/`
2. **User plugins**: 
   - Windows: `%APPDATA%\CLAII\plugins\<plugin_name>\`
   - macOS: `~/Library/Application Support/CLAII/plugins/<plugin_name>/`
   - Linux: `~/.config/CLAII/plugins/<plugin_name>/`

## Managing Plugins

CLAII provides commands for managing plugins:

- `claii system list-plugins` - List all available plugins
- `claii system enable-plugin <name>` - Enable a plugin
- `claii system disable-plugin <name>` - Disable a plugin

## Example Plugins

### Hello World Plugin

Here's a simple "Hello World" plugin that adds a command:

```python
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
```

### Groq AI Model Plugin

Here's a more complex plugin that adds support for the Groq AI API:

```python
"""Groq AI model plugin for CLAII."""

from claii.plugins.base import CLAIIPlugin
from claii.config import load_config
from claii.history import log_history
from claii.prompts.concise import build_prompt
import requests
import json
from rich.console import Console

console = Console()

class GroqPlugin(CLAIIPlugin):
    """Plugin that adds Groq AI model support."""
    
    @property
    def name(self) -> str:
        return "groq"
    
    @property
    def description(self) -> str:
        return "Adds Groq AI model support to CLAII."
    
    @property
    def config_schema(self):
        return {
            "groq_model": {
                "type": "string",
                "default": "llama3-70b-8192",
                "description": "Groq model to use"
            },
            "api_key": {
                "type": "string",
                "description": "Groq API key"
            },
            "temperature": {
                "type": "float",
                "default": 0.7,
                "description": "Temperature for generation"
            },
            "max_tokens": {
                "type": "integer",
                "default": 1024,
                "description": "Maximum tokens to generate"
            }
        }
    
    def get_models(self):
        """Return models provided by this plugin."""
        return [{
            "name": "groq",
            "description": "Groq AI models with fast inference",
            "handler": self.chat_groq
        }]
    
    def chat_groq(self, message: str):
        """Chat with Groq model."""
        if not self.config.get("api_key"):
            return "[red]Groq API key not configured. Use 'claii config set plugins.settings.groq api_key YOUR_API_KEY'[/red]"
        
        model = self.config.get("groq_model", "llama3-70b-8192")
        temperature = self.config.get("temperature", 0.7)
        max_tokens = self.config.get("max_tokens", 1024)
        
        # Apply prompt template
        formatted_prompt = build_prompt(message)
        
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": formatted_prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            console.print(f"[yellow]Using Groq ({model})[/yellow]")
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                log_history(message, content)
                return content
            else:
                error_msg = f"[red]Error from Groq API: {response.status_code} - {response.text}[/red]"
                console.print(error_msg)
                return error_msg
                
        except Exception as e:
            error_msg = f"[red]Error calling Groq API: {str(e)}[/red]"
            console.print(error_msg)
            return error_msg
```

## Best Practices

1. **Unique Names**: Ensure your plugin has a unique name to avoid conflicts.
2. **Error Handling**: Always handle exceptions in your plugin methods to prevent crashes.
3. **Documentation**: Provide clear documentation for your plugin's commands, models, and tools.
4. **Configuration**: Define sensible defaults for configuration options.
5. **Dependencies**: Document any external dependencies that your plugin requires.
6. **Testing**: Create tests to ensure your plugin works as expected.

## Troubleshooting

### Plugin Not Loading

If your plugin isn't loading:

1. Check that it's in the correct directory.
2. Ensure the plugin class inherits from `CLAIIPlugin`.
3. Verify that the `name` property returns a unique name.
4. Look for error messages in the console output.

### Plugin Configuration Issues

If your plugin settings aren't working:

1. Make sure you've enabled the plugin with `claii system enable-plugin <name>`.
2. Check that you're using the correct configuration command format.
3. Verify that your plugin correctly accesses `self.config` in its methods.

## API Reference

### CLAIIPlugin Base Class

The `CLAIIPlugin` base class defines the following methods and properties:

#### Required Properties

- `name` (property): The unique name of the plugin.
- `description` (property): A short description of the plugin.

#### Optional Properties and Methods

- `version` (property): The version of the plugin (default: "0.1.0").
- `config_schema` (property): Schema for plugin configuration (default: empty dict).
- `initialize(config)`: Initialize the plugin with its configuration.
- `get_commands()`: Return list of commands provided by this plugin.
- `get_models()`: Return list of AI models provided by this plugin.
- `get_tools()`: Return list of tools provided by this plugin.
- `on_load()`: Called when the plugin is loaded.
- `on_unload()`: Called when the plugin is unloaded.

## Conclusion

The CLAII Plugin System provides a flexible way to extend CLAII's functionality. By creating plugins, you can add custom commands, integrate new AI models, and provide additional tools to enhance the user experience. 