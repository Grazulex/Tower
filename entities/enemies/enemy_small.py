from typing import List
import pygame
from pygame.surface import Surface
from game.game_manager import GameManager
from entities.enemy_base import EnemyBase
from config.constants import (
    ENEMY_RADIUS,
    ENEMY_SPEED,
    SMALL_ENEMY_RADIUS_MULTIPLIER,
    SMALL_ENEMY_HEALTH,
    SMALL_ENEMY_SPEED_MULTIPLIER,
    SMALL_ENEMY_POINTS,
)
from config.color import GREEN, WHITE
from os.path import join


class EnemySmall(EnemyBase):
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

    def __init__(
        self,
        screen: Surface,
        track_points: List[tuple[int, int]],
        game_manager: GameManager,
    ):
        """
        Initializes an EnemySmall instance.

        Args:
            screen (pygame.Surface): The game screen where the enemy is drawn.
            track_points (list): The points defining the track for enemy movement.
            game_manager (GameManager, optional): The game manager handling game state.
        """
        super().__init__(screen, track_points, game_manager)
        self.color = GREEN
        self.radius = ENEMY_RADIUS * SMALL_ENEMY_RADIUS_MULTIPLIER
        self.text_color = WHITE
        self.health = SMALL_ENEMY_HEALTH
        self.speed = ENEMY_SPEED * SMALL_ENEMY_SPEED_MULTIPLIER
        self.points_value = SMALL_ENEMY_POINTS
        # Load death sound
        self.death_sound = pygame.mixer.Sound(
            join("assets", "sounds", "crystal_bubble_small.wav")
        )

    def play_death_sound(self) -> None:
        """
        Plays the small enemy death sound.
        """
        self.death_sound.play()
