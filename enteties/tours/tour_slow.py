from enteties.tour_base import Tour
from config.color import *
from config.constants import (SLOW_TOWER_RANGE, SLOW_TOWER_ATTACK_SPEED,
                           SLOW_TOWER_DAMAGE, SLOW_TOWER_COST)

class TourSlow(Tour):
    """
    Represents a slow defensive tower in the game.

    Inherits from the base Tour class and modifies attributes to reflect
    its unique characteristics, such as reduced attack speed and increased damage.

    Attributes:
        color (tuple): The color of the tower (RGB format).
        attack_range (int): The range within which the tower can attack enemies.
        attack_speed (float): The attack speed of the tower (attacks per second).
        damage (int): The damage dealt by the tower to enemies.
        cost (int): The cost of the tower.
    """

    def __init__(self, screen, column, row):
        """
        Initializes a TourSlow instance.

        Args:
            screen (pygame.Surface): The game screen where the tower is drawn.
            column (int): The column position of the tower on the grid.
            row (int): The row position of the tower on the grid.
        """
        Tour.__init__(self, screen, column, row)
        self.color = YELLOW
        self.attack_range = SLOW_TOWER_RANGE
        self.attack_speed = SLOW_TOWER_ATTACK_SPEED
        self.damage = SLOW_TOWER_DAMAGE
        self.cost = SLOW_TOWER_COST
