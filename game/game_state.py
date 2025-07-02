"""
game_state.py

This module defines different game states and manages transitions between them.
"""
from typing import Literal

GameStateType = Literal["menu", "playing", "game_over"]
from game.save_manager import save_high_score, load_high_score

class GameState:
    MENU: GameStateType = "menu"
    PLAYING: GameStateType = "playing"
    GAME_OVER: GameStateType = "game_over"

    def __init__(self):
        """Initialize the game state."""
        self.current_state: GameStateType = self.MENU
        self.high_score = load_high_score()

    def get_state(self) -> GameStateType:
        return self.current_state

    def set_state(self, state: GameStateType) -> None:
        self.current_state = state

    def update_high_score(self, score: int) -> bool:
        if score > self.high_score:
            self.high_score = score
            save_high_score(self.high_score)
            return True
        return False

    def get_high_score(self) -> int:
        return self.high_score
