from typing import List
import pygame
from pygame.surface import Surface
from game.game_manager import GameManager
from entities.enemy_base import EnemyBase
from config.constants import (ENEMY_RADIUS, ENEMY_SPEED,
                            BIG_ENEMY_RADIUS_MULTIPLIER, BIG_ENEMY_HEALTH,
                            BIG_ENEMY_SPEED_MULTIPLIER, BIG_ENEMY_POINTS)
from config.color import *
from os.path import join
from dataclasses import dataclass, field

@dataclass
class EnemyBig(EnemyBase):
    screen: Surface
    track_points: List[tuple[int, int]]
    game_manager: GameManager
    color: tuple = field(default=YELLOW, init=False)
    radius: float = field(default=ENEMY_RADIUS * BIG_ENEMY_RADIUS_MULTIPLIER, init=False)
    health: int = field(default=BIG_ENEMY_HEALTH, init=False)
    speed: float = field(default=ENEMY_SPEED * BIG_ENEMY_SPEED_MULTIPLIER, init=False)
    points_value: int = field(default=BIG_ENEMY_POINTS, init=False)
    death_sound: pygame.mixer.Sound = field(init=False)
    """Larger enemy with high health, reduced speed, and higher point value"""

    def __post_init__(self):
        """
        Initializes the EnemyBig instance.

        Sets the initial position based on the first track point and loads the death sound.
        """
        super().__post_init__()
        # Load death sound
        self.death_sound = pygame.mixer.Sound(join('assets', 'sounds', 'crystal_bubble_large.wav'))
