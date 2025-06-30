import pygame
from enteties.tour_base import Tour
from config.color import *
from config.constants import (POWER_TOWER_RANGE, POWER_TOWER_ATTACK_SPEED,
                           POWER_TOWER_DAMAGE, POWER_TOWER_COST)

class TourPower(Tour):
    """
    Represents a powerful defensive tower in the game.

    Inherits from the base Tour class and modifies attributes to reflect
    its unique characteristics, such as increased attack speed and range.

    Attributes:
        color (tuple): The color of the tower (RGB format).
        attack_range (int): The range within which the tower can attack enemies.
        attack_speed (float): The attack speed of the tower (attacks per second).
        damage (int): The damage dealt by the tower to enemies.
        cost (int): The cost of the tower.
    """

    def __init__(self, screen, column, row):
        """
        Initializes a TourPower instance.

        Args:
            screen (pygame.Surface): The game screen where the tower is drawn.
            column (int): The column position of the tower on the grid.
            row (int): The row position of the tower on the grid.
        """
        Tour.__init__(self, screen, column, row)
        self.color = RED
        self.attack_range = POWER_TOWER_RANGE
        self.attack_speed = POWER_TOWER_ATTACK_SPEED
        self.damage = POWER_TOWER_DAMAGE
        self.cost = POWER_TOWER_COST
        # Ne charger le son que si l'écran est défini (pas lors de l'initialisation des types)
        if screen is not None:
            self.attack_sound = pygame.mixer.Sound('assets/sounds/crystal_laser_short.wav')

    def play_attack_sound(self):
        if hasattr(self, 'attack_sound'):
            self.attack_sound.play()
