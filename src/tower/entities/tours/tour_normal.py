import pygame
from tower.entities.tour_base import TourBase
from tower.config.color import BLUE
from tower.config.constants import (
    NORMAL_TOWER_RANGE,
    NORMAL_TOWER_ATTACK_SPEED,
    NORMAL_TOWER_DAMAGE,
    NORMAL_TOWER_COST,
)
from os.path import join
from dataclasses import dataclass, field


@dataclass
class TourNormal(TourBase):
    color: tuple = field(default=BLUE, init=False)
    attack_range: int = field(default=NORMAL_TOWER_RANGE, init=False)
    attack_speed: float = field(default=NORMAL_TOWER_ATTACK_SPEED, init=False)
    damage: int = field(default=NORMAL_TOWER_DAMAGE, init=False)
    cost: int = field(default=NORMAL_TOWER_COST, init=False)
    """Tour with balanced stats for general purpose defense"""

    def __post_init__(self):
        super().__init__(self.screen, self.column, self.row)
        # Only load sound if screen is defined (not during type initialization)
        if self.screen is not None:
            from tower import __file__ as tower_init
            from os.path import dirname
            base_path = dirname(tower_init)
            self.attack_sound = pygame.mixer.Sound(join(base_path, "assets", "sounds", "crystal_laser_medium.wav"))
