import os
HISTORY_PATH = os.path.expanduser("~/.ai-cli-history.log")

def log_history(message: str, reply: str):
    """Log the AI conversation to a history file"""
    with open(HISTORY_PATH, "a") as f:
        f.write(f"Q: {message}\nA: {reply}\n---\n")