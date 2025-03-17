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
        # Check if config is properly initialized
        if not hasattr(self, 'config') or not isinstance(self.config, dict):
            return "[red]Plugin configuration error. Please disable and re-enable the plugin.[/red]"
            
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