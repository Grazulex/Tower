"""
game_state.py

This module defines different game states and manages transitions between them.
"""
from game.save_manager import save_high_score, load_high_score

class GameState:
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"

    def __init__(self):
        self.current_state = self.MENU
        self.high_score = load_high_score()

    def get_state(self):
        return self.current_state

    def set_state(self, state):
        self.current_state = state

    def update_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
            save_high_score(self.high_score)
            return True
        return False

    def get_high_score(self):
        return self.high_score
