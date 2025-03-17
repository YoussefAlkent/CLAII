import os
import importlib
import importlib.util
import inspect
import sys
import logging
from typing import Dict, List, Any, Optional, Type
from pathlib import Path

from claii.plugins.base import CLAIIPlugin
from claii.config import load_config, save_config

logger = logging.getLogger(__name__)

class PluginManager:
    """Manages CLAII plugins."""
    
    def __init__(self):
        self.plugins: Dict[str, CLAIIPlugin] = {}
        self.commands: Dict[str, Dict[str, Any]] = {}
        self.models: Dict[str, Dict[str, Any]] = {}
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.config = load_config()
        
        # Ensure plugins config exists
        if "plugins" not in self.config:
            self.config["plugins"] = {
                "enabled": [],
                "settings": {}
            }
            save_config(self.config)
    
    def discover_plugins(self) -> Dict[str, Type[CLAIIPlugin]]:
        """Discover available plugins in the plugins directory and installed packages."""
        plugin_classes = {}
        
        # Built-in plugins directory
        builtin_plugins_dir = Path(__file__).parent / "builtin"
        if builtin_plugins_dir.exists():
            plugin_classes.update(self._discover_in_directory(builtin_plugins_dir))
        
        # User plugins directory
        user_plugins_dir = None
        if sys.platform == "win32":
            user_plugins_dir = Path(os.environ.get("APPDATA")) / "CLAII" / "plugins"
        elif sys.platform == "darwin":
            user_plugins_dir = Path.home() / "Library" / "Application Support" / "CLAII" / "plugins"
        else:
            user_plugins_dir = Path.home() / ".config" / "CLAII" / "plugins"
        
        if user_plugins_dir and user_plugins_dir.exists():
            plugin_classes.update(self._discover_in_directory(user_plugins_dir))
        
        # TODO: Discover plugins from installed Python packages
        
        return plugin_classes
    
    def _discover_in_directory(self, directory: Path) -> Dict[str, Type[CLAIIPlugin]]:
        """Discover plugins in a directory."""
        plugin_classes = {}
        
        for plugin_dir in directory.iterdir():
            if not plugin_dir.is_dir():
                continue
                
            plugin_init = plugin_dir / "__init__.py"
            if not plugin_init.exists():
                continue
                
            try:
                # Import the module
                module_name = f"claii.plugins.{plugin_dir.name}"
                spec = importlib.util.spec_from_file_location(module_name, plugin_init)
                if not spec or not spec.loader:
                    continue
                    
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find plugin classes
                for _, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and issubclass(obj, CLAIIPlugin) 
                            and obj is not CLAIIPlugin):
                        # Create an instance to get the name
                        try:
                            plugin_instance = obj()
                            plugin_name = str(plugin_instance.name)
                            plugin_classes[plugin_name] = obj
                        except Exception as e:
                            logger.error(f"Error instantiating plugin class {obj.__name__}: {e}")
            
            except Exception as e:
                logger.error(f"Error loading plugin from {plugin_dir}: {e}")
        
        return plugin_classes
    
    def load_plugins(self) -> None:
        """Load all enabled plugins."""
        plugin_classes = self.discover_plugins()
        enabled_plugins = self.config["plugins"]["enabled"]
        
        for plugin_name in enabled_plugins:
            if plugin_name in plugin_classes:
                try:
                    plugin_class = plugin_classes[plugin_name]
                    plugin_instance = plugin_class()
                    
                    # Initialize with config
                    plugin_config = self.config["plugins"]["settings"].get(plugin_name, {})
                    plugin_instance.initialize(plugin_config)
                    
                    # Register plugin
                    self.plugins[plugin_name] = plugin_instance
                    
                    # Register plugin commands, models, and tools
                    self._register_plugin_components(plugin_instance)
                    
                    # Call on_load
                    plugin_instance.on_load()
                    
                    logger.info(f"Loaded plugin: {plugin_name}")
                    
                except Exception as e:
                    logger.error(f"Error initializing plugin {plugin_name}: {e}")
    
    def _register_plugin_components(self, plugin: CLAIIPlugin) -> None:
        """Register a plugin's commands, models, and tools."""
        # Register commands
        for command in plugin.get_commands():
            command_name = command.get("name")
            if command_name:
                self.commands[command_name] = {
                    "plugin": plugin.name,
                    **command
                }
        
        # Register models
        for model in plugin.get_models():
            model_name = model.get("name")
            if model_name:
                self.models[model_name] = {
                    "plugin": plugin.name,
                    **model
                }
        
        # Register tools
        for tool in plugin.get_tools():
            tool_name = tool.get("name")
            if tool_name:
                self.tools[tool_name] = {
                    "plugin": plugin.name,
                    **tool
                }
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable a plugin."""
        plugin_classes = self.discover_plugins()
        
        if plugin_name not in plugin_classes:
            return False
        
        if plugin_name not in self.config["plugins"]["enabled"]:
            self.config["plugins"]["enabled"].append(plugin_name)
            save_config(self.config)
        
        # Load the plugin if it's not already loaded
        if plugin_name not in self.plugins:
            try:
                plugin_class = plugin_classes[plugin_name]
                plugin_instance = plugin_class()
                
                # Initialize with config
                plugin_config = self.config["plugins"]["settings"].get(plugin_name, {})
                plugin_instance.initialize(plugin_config)
                
                # Register plugin
                self.plugins[plugin_name] = plugin_instance
                
                # Register plugin commands, models, and tools
                self._register_plugin_components(plugin_instance)
                
                # Call on_load
                plugin_instance.on_load()
                
                logger.info(f"Loaded plugin: {plugin_name}")
                return True
                
            except Exception as e:
                logger.error(f"Error initializing plugin {plugin_name}: {e}")
                return False
        
        return True
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable a plugin."""
        if plugin_name in self.plugins:
            try:
                # Call on_unload
                self.plugins[plugin_name].on_unload()
                
                # Unregister commands, models, and tools
                self._unregister_plugin_components(plugin_name)
                
                # Remove plugin
                del self.plugins[plugin_name]
                
                logger.info(f"Unloaded plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Error unloading plugin {plugin_name}: {e}")
                return False
        
        # Update config
        if plugin_name in self.config["plugins"]["enabled"]:
            self.config["plugins"]["enabled"].remove(plugin_name)
            save_config(self.config)
        
        return True
    
    def _unregister_plugin_components(self, plugin_name: str) -> None:
        """Unregister a plugin's commands, models, and tools."""
        # Unregister commands
        self.commands = {name: cmd for name, cmd in self.commands.items() 
                        if cmd.get("plugin") != plugin_name}
        
        # Unregister models
        self.models = {name: model for name, model in self.models.items() 
                      if model.get("plugin") != plugin_name}
        
        # Unregister tools
        self.tools = {name: tool for name, tool in self.tools.items() 
                     if tool.get("plugin") != plugin_name}
    
    def get_plugin(self, plugin_name: str) -> Optional[CLAIIPlugin]:
        """Get a plugin by name."""
        return self.plugins.get(plugin_name)
    
    def get_plugin_names(self) -> List[str]:
        """Get names of all loaded plugins."""
        return list(self.plugins.keys())
    
    def get_available_plugin_names(self) -> List[str]:
        """Get names of all available plugins."""
        # Make sure we return strings, not property objects
        return [str(name) for name in self.discover_plugins().keys()]
    
    def get_model_handler(self, model_name: str):
        """Get the handler for a model."""
        if model_name in self.models:
            model_info = self.models[model_name]
            return model_info.get("handler")
        return None
    
    def get_command_handler(self, command_name: str):
        """Get the handler for a command."""
        if command_name in self.commands:
            command_info = self.commands[command_name]
            return command_info.get("handler")
        return None
    
    def get_tool_handler(self, tool_name: str):
        """Get the handler for a tool."""
        if tool_name in self.tools:
            tool_info = self.tools[tool_name]
            return tool_info.get("handler")
        return None

# Create singleton instance
plugin_manager = PluginManager() 