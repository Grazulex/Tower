from enteties.enemy_base import Enemy
from config.color import *
from config.constants import NORMAL_ENEMY_HEALTH, NORMAL_ENEMY_POINTS

class EnemyNormal(Enemy):
    """
    Represents a normal enemy in the game.

    Inherits from the base Enemy class and modifies attributes to reflect
    its unique characteristics, such as moderate health and point value.

    Attributes:
        color (tuple): The color of the enemy (RGB format).
        text_color (tuple): The color of the text displaying the enemy's health.
        health (int): The health of the enemy.
        points_value (int): The points awarded for defeating the enemy.
    """

    def __init__(self, screen, track_points, game_manager):
        """
        Initializes an EnemyNormal instance.

        Args:
            screen (pygame.Surface): The game screen where the enemy is drawn.
            track_points (list): The points defining the track for enemy movement.
            game_manager (GameManager, optional): The game manager handling game state.
        """
        Enemy.__init__(self, screen, track_points, game_manager)
        self.color = BLUE
        self.text_color = WHITE
        self.health = NORMAL_ENEMY_HEALTH
        self.points_value = NORMAL_ENEMY_POINTS
