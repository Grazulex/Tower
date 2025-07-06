import pygame
from pygame.surface import Surface
from enum import Enum, auto
from typing import Optional

from .login_menu import LoginMenu
from .game_ui import GameUI

class GameState(Enum):
    LOGIN = auto()
    PLAYING = auto()

class MenuManager:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.state = GameState.LOGIN
        self.login_menu = LoginMenu(screen)
        self.game_ui = GameUI(screen)
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events based on current state.
        Returns True if the game should start."""
        if self.state == GameState.LOGIN:
            if self.login_menu.handle_event(event):
                self.state = GameState.PLAYING
                return True
        return False
        
    def draw(self) -> None:
        """Draw the current menu/UI based on state."""
        if self.state == GameState.LOGIN:
            self.login_menu.draw()
        # Game UI is handled separately during gameplay
            
    def get_game_ui(self) -> GameUI:
        """Get the game UI instance."""
        return self.game_ui
