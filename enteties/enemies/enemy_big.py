import pygame
from enteties.enemy_base import Enemy
from config.constants import (ENEMY_RADIUS, ENEMY_SPEED,
                            BIG_ENEMY_RADIUS_MULTIPLIER, BIG_ENEMY_HEALTH,
                            BIG_ENEMY_SPEED_MULTIPLIER, BIG_ENEMY_POINTS)
from config.color import *


class EnemyBig(Enemy):
    """
    Represents a larger and slower enemy in the game.

    Inherits from the base Enemy class and modifies attributes to reflect
    its unique characteristics, such as increased health, reduced speed,
    and higher point value.

    Attributes:
        color (tuple): The color of the enemy (RGB format).
        radius (float): The radius of the enemy's representation.
        health (int): The health of the enemy.
        speed (float): The speed of the enemy's movement.
        points_value (int): The points awarded for defeating the enemy.
    """

    def __init__(self, screen, track_points, game_manager):
        """
        Initializes an EnemyBig instance.

        Args:
            screen (pygame.Surface): The game screen where the enemy is drawn.
            track_points (list): The points defining the track for enemy movement.
            game_manager (GameManager, optional): The game manager handling game state.
        """
        Enemy.__init__(self, screen, track_points, game_manager)
        self.color = YELLOW
        self.radius = ENEMY_RADIUS * BIG_ENEMY_RADIUS_MULTIPLIER
        self.health = BIG_ENEMY_HEALTH
        self.speed = ENEMY_SPEED * BIG_ENEMY_SPEED_MULTIPLIER
        self.points_value = BIG_ENEMY_POINTS
        # Charger le son de mort
        self.death_sound = pygame.mixer.Sound('assets/sounds/crystal_bubble_large.wav')

    def play_death_sound(self):
        """
        Joue le son de mort de l'ennemi grand.
        """
        self.death_sound.play()
