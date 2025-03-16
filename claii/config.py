import os
import json
import platform
from pathlib import Path

# CONFIG_PATH = os.path.expanduser("~/.config/CLAII/config.json")

if platform.system() == "Windows":
    CONFIG_PATH = Path(os.getenv("APPDATA")) / "CLAII" / "config.json"
elif platform.system() == "Darwin":
    CONFIG_PATH = Path.home() / "Library" / "Application Support" / "CLAII" / "config.json"
else:
    CONFIG_PATH = Path.home() / ".config" / "CLAII" / "config.json"

def ensure_config_dir():
    """Ensure configuration directory exists"""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

def load_config():
    """Load configuration file"""
    ensure_config_dir()
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    """Save configuration to file"""
    ensure_config_dir()
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
