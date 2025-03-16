import pytest
from claii.config import load_config, save_config

def test_save_and_load_config(tmp_path):
    """Test saving and loading config"""
    config_file = tmp_path / "config.json"
    save_config({"tool": "ollama"}, config_file)
    config = load_config(config_file)
    assert config["tool"] == "ollama"