"""
save_manager.py

This module handles saving and loading game data.
"""

from typing import Dict
import json
import os

SAVE_FILE = "save_data.json"


def save_high_score(score: int) -> None:
    """
    Saves the high score to a file.

    Args:
        score (int): The score to save
    """
    data: Dict[str, int] = {"high_score": score}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)


def load_high_score() -> int:
    """
    Loads the high score from the file.

    Returns:
        int: The loaded high score, 0 if no file exists
    """
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
    except (json.JSONDecodeError, IOError):
        pass
    return 0
