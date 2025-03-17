from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class CLAIIPlugin(ABC):
    """Base class for all CLAII plugins."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the plugin."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """A short description of the plugin."""
        pass
    
    @property
    def version(self) -> str:
        """The version of the plugin."""
        return "0.1.0"
    
    @property
    def config_schema(self) -> Dict[str, Any]:
        """Schema for plugin configuration."""
        return {}
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin with its configuration."""
        self.config = config
    
    def get_commands(self) -> List[Dict[str, Any]]:
        """Return list of commands provided by this plugin."""
        return []
    
    def get_models(self) -> List[Dict[str, Any]]:
        """Return list of AI models provided by this plugin."""
        return []
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of tools provided by this plugin."""
        return []
    
    def on_load(self) -> None:
        """Called when the plugin is loaded."""
        pass
    
    def on_unload(self) -> None:
        """Called when the plugin is unloaded."""
        pass 