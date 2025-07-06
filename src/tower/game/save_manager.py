"""
save_manager.py

This module handles saving and loading game data.
"""

from typing import Dict, List
from tower.game.player import PlayerManager


def save_high_score(score: int) -> None:
    """
    Saves the high score by updating the current player's scores.

    Args:
        score (int): The score to save
    """
    current_player = PlayerManager.get_current_player()
    if current_player:
        PlayerManager.save_score(score)


def load_high_score() -> int:
    """
    Loads the highest score from all players.

    Returns:
        int: The highest score, 0 if no scores exist
    """
    all_scores = get_all_high_scores()
    if all_scores:
        return max(score["high_score"] for score in all_scores)
    return 0


def get_all_high_scores() -> List[Dict[str, any]]:
    """
    Gets all players' high scores.

    Returns:
        List[Dict[str, any]]: List of player scores, sorted by highest score
    """
    players = PlayerManager.load_players()
    scores_list = []

    for username, player in players.items():
        if player.scores:
            scores_list.append({"username": username, "high_score": max(player.scores)})

    return sorted(scores_list, key=lambda x: x["high_score"], reverse=True)
