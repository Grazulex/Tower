import pygame
from tower.entities.enemy_base import EnemyBase
from tower.config.constants import (
    ENEMY_RADIUS,
    ENEMY_SPEED,
    BIG_ENEMY_RADIUS_MULTIPLIER,
    BIG_ENEMY_HEALTH,
    BIG_ENEMY_SPEED_MULTIPLIER,
    BIG_ENEMY_POINTS,
)
from tower.config.color import YELLOW
from os.path import join
from dataclasses import dataclass, field


@dataclass
class EnemyBig(EnemyBase):
    color: tuple = field(default=YELLOW, init=False)
    radius: float = field(default=ENEMY_RADIUS * BIG_ENEMY_RADIUS_MULTIPLIER, init=False)
    health: int = field(default=BIG_ENEMY_HEALTH, init=False)
    speed: float = field(default=ENEMY_SPEED * BIG_ENEMY_SPEED_MULTIPLIER, init=False)
    points_value: int = field(default=BIG_ENEMY_POINTS, init=False)
    """Larger enemy with high health, reduced speed, and higher point value"""

    def __post_init__(self):
        """
        Initializes the EnemyBig instance.

        Sets the initial position based on the first track point and loads the death sound.
        """
        super().__post_init__()
        # Load death sound
        try:
            from tower import __file__ as tower_init
            from os.path import dirname
            base_path = dirname(tower_init)
            self.death_sound = pygame.mixer.Sound(join(base_path, "assets", "sounds", "crystal_bubble_large.wav"))
        except (pygame.error, ImportError):
            pass  # Skip sound initialization if audio is not available
