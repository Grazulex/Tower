from typing import List
import pygame
from pygame.surface import Surface
from game.game_manager import GameManager
from enteties.enemy_base import EnemyBase
from config.constants import (ENEMY_RADIUS, ENEMY_SPEED,
                            BIG_ENEMY_RADIUS_MULTIPLIER, BIG_ENEMY_HEALTH,
                            BIG_ENEMY_SPEED_MULTIPLIER, BIG_ENEMY_POINTS)
from config.color import *
from os.path import join


class EnemyBig(EnemyBase):
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

    def __init__(self, screen: Surface, track_points: List[tuple[int, int]], game_manager: GameManager):
        """
        Initializes an EnemyBig instance.

        Args:
            screen (pygame.Surface): The game screen where the enemy is drawn.
            track_points (list): The points defining the track for enemy movement.
            game_manager (GameManager, optional): The game manager handling game state.
        """
        super().__init__(screen, track_points, game_manager)
        self.color = YELLOW
        self.radius = ENEMY_RADIUS * BIG_ENEMY_RADIUS_MULTIPLIER
        self.health = BIG_ENEMY_HEALTH
        self.speed = ENEMY_SPEED * BIG_ENEMY_SPEED_MULTIPLIER
        self.points_value = BIG_ENEMY_POINTS
        # Load death sound
        self.death_sound = pygame.mixer.Sound(join('assets','sounds','crystal_bubble_large.wav'))

    def play_death_sound(self) -> None:
        """
        Plays the big enemy death sound.
        """
        self.death_sound.play()
