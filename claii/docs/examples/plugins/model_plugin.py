"""
Example AI Model Plugin for CLAII

This is an example plugin that adds a custom AI model to CLAII.
"""

from claii.plugins.base import CLAIIPlugin
from claii.history import log_history
import random

class EchoModelPlugin(CLAIIPlugin):
    """A simple echo model plugin for CLAII."""
    
    @property
    def name(self) -> str:
        return "echo_model"
    
    @property
    def description(self) -> str:
        return "A simple echo AI model for demonstration."
    
    @property
    def version(self) -> str:
        return "0.1.0"
    
    @property
    def config_schema(self):
        """Schema for plugin configuration."""
        return {
            "prefix": {
                "type": "string",
                "default": "Echo: ",
                "description": "Prefix to add to responses"
            },
            "random_mode": {
                "type": "boolean",
                "default": False,
                "description": "Randomly modify responses"
            }
        }
    
    def get_models(self):
        """Return models provided by this plugin."""
        return [{
            "name": "echo",
            "description": "Simple echo AI model",
            "handler": self.echo_model_handler
        }]
    
    def echo_model_handler(self, message: str):
        """Handler for the echo model."""
        # Get configuration options
        prefix = self.config.get("prefix", "Echo: ")
        random_mode = self.config.get("random_mode", False)
        
        # Create the response
        if random_mode:
            # Add some randomness
            words = message.split()
            if words:
                random.shuffle(words)
                response = f"{prefix}{' '.join(words)}"
            else:
                response = f"{prefix}{message}"
        else:
            # Simple echo
            response = f"{prefix}{message}"
        
        # Log the interaction
        log_history(message, response)
        
        return response 