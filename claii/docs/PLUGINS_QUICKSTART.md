# CLAII Plugin System Quickstart Guide

This quickstart guide will help you get started with the CLAII plugin system. For more detailed documentation, refer to the [plugins.md](plugins.md) file.

## Installing a Plugin

To install a plugin:

1. Create a directory for your plugin:
   - Built-in plugins: `claii/plugins/builtin/your_plugin_name/`
   - User plugins: 
     - macOS: `~/Library/Application Support/CLAII/plugins/your_plugin_name/`
     - Linux: `~/.config/CLAII/plugins/your_plugin_name/`
     - Windows: `%APPDATA%\CLAII\plugins\your_plugin_name\`

2. Place your plugin files in the directory. At minimum, you need an `__init__.py` file containing your plugin class.

## Creating a Simple Plugin

Here's a minimal plugin example:

```python
from claii.plugins.base import CLAIIPlugin

class MyPlugin(CLAIIPlugin):
    @property
    def name(self) -> str:
        return "my_plugin"
    
    @property
    def description(self) -> str:
        return "My first CLAII plugin"
```

## Enabling a Plugin

To enable a plugin, use the following command:

```
claii system enable-plugin my_plugin
```

## Managing Plugins

Here are some useful commands for managing plugins:

- List all available plugins:
  ```
  claii system list-plugins
  ```

- Enable a plugin:
  ```
  claii system enable-plugin my_plugin
  ```

- Disable a plugin:
  ```
  claii system disable-plugin my_plugin
  ```

## Configuring a Plugin

To configure a plugin, use the following command format:

```
claii config set plugins.settings.my_plugin setting_name value
```

For example:

```
claii config set plugins.settings.groq api_key your_api_key
claii config set plugins.settings.groq groq_model llama3-70b-8192
```

## Using a Plugin Model

To use an AI model provided by a plugin:

```
claii chat "Your message" --tool model_name
```

For example:

```
claii chat "Tell me a joke" --tool groq
```

## Plugin Development Workflow

1. Create a new plugin directory in `claii/plugins/builtin/`
2. Create an `__init__.py` file with your plugin class
3. Implement required methods (name, description) and any optional methods (get_commands, get_models, get_tools)
4. Enable your plugin with `claii system enable-plugin your_plugin_name`
5. Test your plugin's functionality
6. Configure your plugin if needed

## Example Plugins

Check out the example plugins in the `docs/examples/plugins/` directory:

- `hello_plugin.py` - Simple command plugin
- `model_plugin.py` - AI model plugin
- `tool_plugin.py` - Tool plugin

## Next Steps

- Read the full [plugins.md](plugins.md) documentation
- Explore the example plugins
- Try creating your own plugin 