import pygame
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
from dataclasses import dataclass, field


@dataclass
class EnemySmall(EnemyBase):
    color: tuple = field(default=GREEN, init=False)
    radius: float = field(default=ENEMY_RADIUS * SMALL_ENEMY_RADIUS_MULTIPLIER, init=False)
    text_color: tuple = field(default=WHITE, init=False)
    health: int = field(default=SMALL_ENEMY_HEALTH, init=False)
    speed: float = field(default=ENEMY_SPEED * SMALL_ENEMY_SPEED_MULTIPLIER, init=False)
    points_value: int = field(default=SMALL_ENEMY_POINTS, init=False)
    """Small and fast enemy with reduced health"""

    def __post_init__(self):
        """
        Initializes the EnemySmall instance.

        Sets the initial position based on the first track point and loads the death sound.
        """
        super().__post_init__()
        # Load death sound
        self.death_sound = pygame.mixer.Sound(join("assets", "sounds", "crystal_bubble_small.wav"))
