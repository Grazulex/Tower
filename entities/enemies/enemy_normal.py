from typing import List
import pygame
from pygame.surface import Surface
from game.game_manager import GameManager
from entities.enemy_base import EnemyBase
from config.color import BLUE, WHITE
from config.constants import NORMAL_ENEMY_HEALTH, NORMAL_ENEMY_POINTS
from os.path import join


class EnemyNormal(EnemyBase):
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

    def __init__(
        self,
        screen: Surface,
        track_points: List[tuple[int, int]],
        game_manager: GameManager,
    ):
        """
        Initializes an EnemyNormal instance.

        Args:
            screen (pygame.Surface): The game screen where the enemy is drawn.
            track_points (list): The points defining the track for enemy movement.
            game_manager (GameManager, optional): The game manager handling game state.
        """
        super().__init__(screen, track_points, game_manager)
        self.color = BLUE
        self.text_color = WHITE
        self.health = NORMAL_ENEMY_HEALTH
        self.points_value = NORMAL_ENEMY_POINTS
        # Load death sound
        self.death_sound = pygame.mixer.Sound(
            join("assets", "sounds", "crystal_bubble_medium.wav")
        )

    def play_death_sound(self) -> None:
        """
        Plays the normal enemy death sound.
        """
        self.death_sound.play()
