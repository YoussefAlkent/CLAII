# CLAII Plugin System

CLAII's plugin system allows you to extend the functionality of the CLI with custom commands, AI models, and tools.

## Plugin Structure

Each plugin is a Python package with the following structure:

```
my_plugin/
  __init__.py  # Main plugin file with CLAIIPlugin class
  ... other files ...
```

The `__init__.py` file must contain a class that inherits from `CLAIIPlugin` and implements the required methods.

## Creating a Plugin

To create a plugin, you need to:

1. Create a new directory for your plugin
2. Create an `__init__.py` file with a class that inherits from `CLAIIPlugin`
3. Implement the required methods

Example:

```python
from claii.plugins.base import CLAIIPlugin

class MyPlugin(CLAIIPlugin):
    @property
    def name(self) -> str:
        return "my_plugin"
    
    @property
    def description(self) -> str:
        return "My awesome plugin"
    
    # Other methods...
```

## Installing Plugins

Plugins can be installed in one of these locations:

1. Built-in plugins: `claii/plugins/builtin/<plugin_name>/`
2. User plugins: 
   - Windows: `%APPDATA%\CLAII\plugins\<plugin_name>\`
   - macOS: `~/Library/Application Support/CLAII/plugins/<plugin_name>/`
   - Linux: `~/.config/CLAII/plugins/<plugin_name>/`

## Managing Plugins

Use the following commands to manage plugins:

- `claii system list-plugins` - List all available plugins
- `claii system enable-plugin NAME` - Enable a plugin
- `claii system disable-plugin NAME` - Disable a plugin

## Plugin Types

Plugins can extend CLAII in several ways:

### Commands

Add new CLI commands to CLAII:

```python
def get_commands(self):
    return [{
        "name": "hello",
        "description": "Say hello",
        "handler": self.hello_command
    }]

def hello_command(self):
    typer_app = typer.Typer()
    
    @typer_app.command()
    def world(name: str = typer.Option("World")):
        """Say hello to someone."""
        typer.echo(f"Hello, {name}!")
    
    return typer_app
```

### AI Models

Add new AI models to CLAII:

```python
def get_models(self):
    return [{
        "name": "claude",
        "description": "Claude AI model",
        "handler": self.chat_claude
    }]

def chat_claude(self, message: str):
    # Implement model chat function
    return "Response from Claude"
```

### Tools

Add new tools to CLAII:

```python
def get_tools(self):
    return [{
        "name": "translate",
        "description": "Translate text",
        "handler": self.translate_tool
    }]

def translate_tool(self, text: str, lang: str):
    # Implement tool function
    return f"Translated: {text}"
```

## Configuration

Plugins can define their configuration schema:

```python
@property
def config_schema(self):
    return {
        "api_key": {
            "type": "string",
            "description": "API key for the service"
        },
        "model": {
            "type": "string",
            "default": "default-model",
            "description": "Model to use"
        }
    }
```

Users can configure plugins using:

```
claii config set plugins.settings.my_plugin.api_key MY_API_KEY
``` 