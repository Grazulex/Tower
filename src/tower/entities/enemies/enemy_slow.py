import pygame
from tower.entities.enemy_base import EnemyBase
from tower.config.constants import (
    ENEMY_RADIUS,
    ENEMY_SPEED,
    SLOW_ENEMY_RADIUS_MULTIPLIER,
    SLOW_ENEMY_HEALTH,
    SLOW_ENEMY_SPEED_MULTIPLIER,
    SLOW_ENEMY_POINTS,
)
from tower.config.color import PURPLE, BLACK
from os.path import join
from dataclasses import dataclass, field


@dataclass
class EnemySlow(EnemyBase):
    color: tuple = field(default=PURPLE, init=False)
    radius: float = field(default=ENEMY_RADIUS * SLOW_ENEMY_RADIUS_MULTIPLIER, init=False)
    text_color: tuple = field(default=BLACK, init=False)
    health: int = field(default=SLOW_ENEMY_HEALTH, init=False)
    speed: float = field(default=ENEMY_SPEED * SLOW_ENEMY_SPEED_MULTIPLIER, init=False)
    points_value: int = field(default=SLOW_ENEMY_POINTS, init=False)
    """Slow enemy with higher defense but reduced speed"""

    def __post_init__(self):
        """
        Initializes the EnemySlow instance.

        Sets the initial position based on the first track point and loads the death sound.
        """
        super().__post_init__()
        # Load death sound
        from tower import __file__ as tower_init
        from os.path import dirname
        base_path = dirname(tower_init)
        self.death_sound = pygame.mixer.Sound(join(base_path, "assets", "sounds", "crystal_bubble_small.wav"))
