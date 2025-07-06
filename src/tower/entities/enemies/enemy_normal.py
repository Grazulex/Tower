import pygame
from tower.entities.enemy_base import EnemyBase
from tower.config.color import BLUE, WHITE
from tower.config.constants import NORMAL_ENEMY_HEALTH, NORMAL_ENEMY_POINTS
from os.path import join
from dataclasses import dataclass, field


@dataclass
class EnemyNormal(EnemyBase):
    color: tuple = field(default=BLUE, init=False)
    text_color: tuple = field(default=WHITE, init=False)
    health: int = field(default=NORMAL_ENEMY_HEALTH, init=False)
    points_value: int = field(default=NORMAL_ENEMY_POINTS, init=False)
    """Standard enemy with balanced health and point value"""

    def __post_init__(self):
        """
        Initializes the EnemyNormal instance.

        Sets the initial position based on the first track point and loads the death sound.
        """
        super().__post_init__()
        # Load death sound
        from tower import __file__ as tower_init
        from os.path import dirname
        base_path = dirname(tower_init)
        self.death_sound = pygame.mixer.Sound(join(base_path, "assets", "sounds", "crystal_bubble_medium.wav"))
