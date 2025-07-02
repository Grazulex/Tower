from typing import Optional
import pygame
from pygame.surface import Surface
from enteties.tour_base import TourBase
from config.color import *
from config.constants import (NORMAL_TOWER_RANGE, NORMAL_TOWER_ATTACK_SPEED,
                           NORMAL_TOWER_DAMAGE, NORMAL_TOWER_COST)
from os.path import join

class TourNormal(TourBase):
    """
    Represents a normal defensive tower in the game.

    Inherits from the base Tour class and modifies attributes to reflect
    its unique characteristics, such as its color.

    Attributes:
        color (tuple): The color of the tower (RGB format).
    """

    def __init__(self, screen: Optional[Surface], column: int, row: int):
        """
        Initializes a TourNormal instance.

        Args:
            screen (pygame.Surface): The game screen where the tower is drawn.
            column (int): The column position of the tower on the grid.
            row (int): The row position of the tower on the grid.
        """
        super().__init__(screen, column, row)
        self.color = BLUE
        self.attack_range = NORMAL_TOWER_RANGE
        self.attack_speed = NORMAL_TOWER_ATTACK_SPEED
        self.damage = NORMAL_TOWER_DAMAGE
        self.cost = NORMAL_TOWER_COST
        # Only load sound if screen is defined (not during type initialization)
        if screen is not None:
            self.attack_sound = pygame.mixer.Sound(join('assets','sounds','crystal_laser_medium.wav'))

    def play_attack_sound(self) -> None:
        if hasattr(self, 'attack_sound'):
            self.attack_sound.play()
