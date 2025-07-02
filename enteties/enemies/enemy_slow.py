import pygame
from enteties.enemy_base import Enemy
from config.constants import (ENEMY_RADIUS, ENEMY_SPEED,
                            SLOW_ENEMY_RADIUS_MULTIPLIER, SLOW_ENEMY_HEALTH,
                            SLOW_ENEMY_SPEED_MULTIPLIER, SLOW_ENEMY_POINTS)
from config.color import *
from os.path import join


class EnemySlow(Enemy):
    """
    Represents a smaller and faster enemy in the game.

    Inherits from the base Enemy class and modifies attributes to reflect
    its unique characteristics, such as reduced health, increased speed,
    and moderate point value.

    Attributes:
        color (tuple): The color of the enemy (RGB format).
        radius (float): The radius of the enemy's representation.
        text_color (tuple): The color of the text displaying the enemy's health.
        health (int): The health of the enemy.
        speed (float): The speed of the enemy's movement.
        points_value (int): The points awarded for defeating the enemy.
    """

    def __init__(self, screen, track_points, game_manager):
        """
        Initializes an EnemySmall instance.

        Args:
            screen (pygame.Surface): The game screen where the enemy is drawn.
            track_points (list): The points defining the track for enemy movement.
            game_manager (GameManager, optional): The game manager handling game state.
        """
        Enemy.__init__(self, screen, track_points, game_manager)
        self.color = PURPLE
        self.radius = ENEMY_RADIUS * SLOW_ENEMY_RADIUS_MULTIPLIER
        self.text_color = BLACK
        self.health = SLOW_ENEMY_HEALTH
        self.speed = ENEMY_SPEED * SLOW_ENEMY_SPEED_MULTIPLIER
        self.points_value = SLOW_ENEMY_POINTS
        # Charger le son de mort
        self.death_sound = pygame.mixer.Sound(join('assets','sounds','crystal_bubble_small.wav'))

    def play_death_sound(self):
        """
        Joue le son de mort de l'ennemi petit.
        """
        self.death_sound.play()
